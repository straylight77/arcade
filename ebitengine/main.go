package main

// Assets: https://kenney.nl/assets/space-shooter-redux
// Fonts: https://www.kenney.nl/assets/kenney-fonts

import (
	"embed"
	"fmt"
	"image/color"
	"log"
	"math/rand"

	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/ebitenutil"
	"github.com/hajimehoshi/ebiten/v2/text"
	"github.com/hajimehoshi/ebiten/v2/vector"
	"golang.org/x/image/font"
)

const MAX_X = 1024
const MAX_Y = 768

//go:embed assets/*
var assets embed.FS

var playerLifeImg *ebiten.Image

func init() {
	playerLifeImg = MustLoadImage("assets/playerLife1_blue.png")
}

/**************************************************************************
 *                                  Game                                  *
 **************************************************************************/
type Game struct {
	Done      bool
	Debug     bool
	Level     int
	Score     int
	Lives     int
	player    *Player
	asteroids []*Asteroid
	shots     []*Shot
	controls  Controls
	Font      font.Face
	wait      int
}

// ------------------------------------------------------------------------
func (g *Game) Init() {
	g.Font = loadFont("assets/font.ttf")
	g.controls = Controls{}
	g.controls.Init()
	g.player = MakePlayer()
	g.Reset()
}

// ------------------------------------------------------------------------
func (g *Game) Reset() {
	g.player.Reset()
	g.Level = 1
	g.Score = 0
	g.Lives = 3
	g.asteroids = make([]*Asteroid, 0)
	g.makeLevel()
	g.killAllShots()
}

// ------------------------------------------------------------------------
func (g *Game) Update() error {

	g.controls.handleInput()

	if g.controls.Cmd["quit"] == 1 {
		return ebiten.Termination
	}

	if g.controls.Cmd["debug"] == 1 {
		g.Debug = !g.Debug
		g.controls.Cmd["debug"] = 0
	}

	if g.wait > 0 {
		g.wait--
		return nil
	}

	if g.controls.Cmd["fire"] == 1 {
		g.controls.Cmd["fire"] = 0
		if g.Lives > 0 {
			// create a new shot
			s := MakeShotFromPlayer(g.player)
			g.shots = append(g.shots, s)
		} else {
			// restart the game
			g.Reset()
		}

	}

	if g.Lives > 0 {
		g.player.Update(MAX_X, MAX_Y, g.controls)
	}

	for _, a := range g.asteroids {
		a.Update(MAX_X, MAX_Y)
	}
	for _, s := range g.shots {
		s.Update(MAX_X, MAX_Y)
	}

	for i, s := range g.shots {
		if s.IsDead() {
			g.shots = append(g.shots[:i], g.shots[i+1:]...)
			break
		}
	}

	// Asteroid-Shot collision detection
	var new_asteroids []*Asteroid

	for i, s := range g.shots {
		for j, a := range g.asteroids {

			if s.IntersectsWith(a) {
				g.Score += 100
				if a.Stage > 1 {
					a1, a2 := a.Split()
					new_asteroids = append(new_asteroids, a1, a2)
				}
				g.shots = append(g.shots[:i], g.shots[i+1:]...)
				g.asteroids = append(g.asteroids[:j], g.asteroids[j+1:]...)
			}
		}
	}
	if len(new_asteroids) > 0 {
		g.asteroids = append(g.asteroids, new_asteroids...)
	}

	// Asteroid-Player collision detection
	if g.player.Invincible <= 0 && g.Lives > 0 {
		for _, a := range g.asteroids {
			if a.IntersectsWith(g.player) {
				g.Lives--
				if g.Lives > 0 {
					g.player.Reset()
				}
			}
		}
	}

	// Check for end of level
	if len(g.asteroids) == 0 {
		g.player.Reset()
		g.Level++
		g.makeLevel()
		g.killAllShots()
		g.wait = 60 * 3
	}

	return nil
}

// ------------------------------------------------------------------------
func (g *Game) Draw(screen *ebiten.Image) {
	for _, s := range g.shots {
		if !s.IsDead() {
			s.Draw(screen)
		}
	}

	for _, a := range g.asteroids {
		a.Draw(screen)
	}

	if g.Lives > 0 {
		g.player.Draw(screen)
	}

	// draw score
	text.Draw(screen, fmt.Sprintf("%06d", g.Score), g.Font, MAX_X/2-115, 50, color.White)
	text.Draw(screen, fmt.Sprintf("%02d", g.Level), g.Font, MAX_X-100, 50, color.White)

	if g.wait > 0 && g.wait%16 > 8 {
		text.Draw(screen, fmt.Sprintf("Level %d", g.Level), g.Font, MAX_X/2-140, MAX_Y/2-50, color.White)
	}

	// draw images for number of lives left
	for i := 0; i < g.Lives-1; i++ {
		op := &ebiten.DrawImageOptions{}
		op.GeoM.Translate(float64(30+(40*i)), 25)
		screen.DrawImage(playerLifeImg, op)
	}

	if g.Lives <= 0 {
		text.Draw(screen, "GAME OVER", g.Font, MAX_X/2-140, MAX_Y/2-50, color.White)
	}

	g.drawDebug(screen)
}

// ------------------------------------------------------------------------
func (g *Game) Layout(outsideWidth, outsideHeight int) (screenWidth, screenHeight int) {
	return MAX_X, MAX_Y
}

// ------------------------------------------------------------------------
func (g *Game) drawDebug(screen *ebiten.Image) {
	if !g.Debug {
		return
	}

	msg := fmt.Sprintf(
		"FPS: %.1f  TPS: %.1f\n\nControls: %v\n\nPlayer: %v\nInvincible: %v",
		ebiten.ActualFPS(),
		ebiten.ActualTPS(),
		g.controls.Cmd,
		g.player,
		g.player.Invincible,
	)
	ebitenutil.DebugPrintAt(screen, msg, 0, 100)

	for i, v := range g.shots {
		msg := fmt.Sprintf("%d: %v", i, v)
		ebitenutil.DebugPrintAt(screen, msg, 0, 200+(i*20))
	}

	for _, obj := range g.asteroids {
		g.drawHitbox(screen, obj)
	}
	for _, obj := range g.shots {
		g.drawHitbox(screen, obj)
	}
	g.drawHitbox(screen, g.player)

}

// ------------------------------------------------------------------------
func (g *Game) drawHitbox(screen *ebiten.Image, obj Sprite) {
	x64, y64 := obj.GetPos()
	x := float32(x64)
	y := float32(y64)
	r := float32(obj.GetRadius())
	vector.StrokeCircle(screen, x, y, r, 1, color.White, true)
}

// ------------------------------------------------------------------------
func (g *Game) killAllShots() {
	g.shots = make([]*Shot, 0)
}

// ------------------------------------------------------------------------
func (g *Game) makeLevel() {
	num := (g.Level-1)/2 + 1
	stage := 3 - (g.Level % 2)
	for i := 0; i < num; i++ {
		dir := getRandDirection()
		spd := getRandSpeed()
		x := float64(rand.Intn(MAX_X))
		y := float64(rand.Intn(MAX_Y))
		a := MakeAsteroid(stage, x, y, dir, spd)
		g.asteroids = append(g.asteroids, a)
	}
}

/**************************************************************************
 *                                   MAIN                                 *
 **************************************************************************/
func main() {
	game := Game{}
	game.Init()

	ebiten.SetWindowSize(MAX_X, MAX_Y)
	ebiten.SetWindowTitle("Asteroids!")
	if err := ebiten.RunGame(&game); err != nil {
		log.Fatal(err)
	}
}
