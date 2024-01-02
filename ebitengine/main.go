package main

// Assets: https://kenney.nl/assets/space-shooter-redux

import (
	"fmt"
	"image/color"
	"log"
	"math/rand"

	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/ebitenutil"
	"github.com/hajimehoshi/ebiten/v2/vector"
)

const MAX_X = 1024
const MAX_Y = 768

/**************************************************************************
 *                                  Game                                  *
 **************************************************************************/
type Game struct {
	Done      bool
	Debug     bool
	Level     int
	Score     int
	player    *Player
	asteroids []*Asteroid
	shots     []*Shot
	controls  Controls
}

// ------------------------------------------------------------------------
func (g *Game) Init() {
	g.controls = Controls{}
	g.controls.Init()
	g.player = MakePlayer()
	g.Level = 1
	g.Score = 0
	g.makeLevel()
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

	if g.controls.Cmd["fire"] == 1 {
		// create a new shot
		s := MakeShotFromPlayer(g.player)
		g.shots = append(g.shots, s)
		g.controls.Cmd["fire"] = 0
	}

	for _, a := range g.asteroids {
		a.Update(MAX_X, MAX_Y)
	}
	for _, s := range g.shots {
		s.Update(MAX_X, MAX_Y)
	}
	g.player.Update(MAX_X, MAX_Y, g.controls)

	for i, s := range g.shots {
		if s.IsDead() {
			g.shots = append(g.shots[:i], g.shots[i+1:]...)
			break
		}
	}

	// do collision detection
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

	return nil
}

// ------------------------------------------------------------------------
func (g *Game) Draw(screen *ebiten.Image) {
	for _, s := range g.shots {
		s.Draw(screen)
	}
	for _, a := range g.asteroids {
		a.Draw(screen)
	}
	g.player.Draw(screen)
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
		"FPS: %.1f  TPS: %.1f\n\nCMD: %v\n\nPlayer: %v\nScore: %v",
		ebiten.ActualFPS(),
		ebiten.ActualTPS(),
		g.controls.Cmd,
		g.player,
		g.Score,
	)
	ebitenutil.DebugPrint(screen, msg)

	for i, v := range g.shots {
		msg := fmt.Sprintf("%d: %v", i, v)
		ebitenutil.DebugPrintAt(screen, msg, 0, 100+(i*20))
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
func (g *Game) makeLevel() {
	//num := (g.level-1)/2 + 1
	//stage := 3 - (g.level % 2)
	num := 3
	for i := 0; i < num; i++ {
		dir := getRandDirection()
		spd := getRandSpeed()
		x := float64(rand.Intn(MAX_X))
		y := float64(rand.Intn(MAX_Y))
		a := MakeAsteroid(3, x, y, dir, spd)
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
