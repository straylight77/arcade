package main

// Assets: https://kenney.nl/assets/space-shooter-redux

import (
	"fmt"
	"log"
	"math"
	"math/rand"

	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/ebitenutil"
)

const MAX_X = 1024
const MAX_Y = 768

/**************************************************************************
 *                                  Game                                  *
 **************************************************************************/
type Game struct {
	Done      bool
	Debug     bool
	level     int
	player    Player
	asteroids []*Asteroid
	shots     []*Shot
	controls  Controls
}

// ------------------------------------------------------------------------
func (g *Game) Init() {
	g.controls = Controls{}
	g.controls.Init()
	g.player = MakePlayer()
	g.level = 1
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
		s := MakeShotFromPlayer(&g.player)
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
	for i, s := range g.shots {
		for j, a := range g.asteroids {
			dx := s.X - a.X
			dy := s.Y - a.Y
			dist := math.Sqrt(dx*dx + dy*dy)
			intersects := dist < a.Radius

			if intersects {
				g.shots = append(g.shots[:i], g.shots[i+1:]...)
				g.asteroids = append(g.asteroids[:j], g.asteroids[j+1:]...)
			}
		}
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
		"FPS: %.1f  TPS: %.1f\n\nCMD: %v\n\nPlayer: %v",
		ebiten.ActualFPS(),
		ebiten.ActualTPS(),
		g.controls.Cmd,
		g.player,
	)
	ebitenutil.DebugPrint(screen, msg)

	for i, v := range g.shots {
		msg := fmt.Sprintf("%d: %v", i, v)
		ebitenutil.DebugPrintAt(screen, msg, 0, 100+(i*20))
	}
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
		a := MakeAsteroid(x, y, dir, spd)
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
