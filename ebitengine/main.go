package main

// Assets: https://kenney.nl/assets/space-shooter-redux

import (
	"fmt"
	"log"
	"math/rand"

	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/ebitenutil"
	//https://github.com/fogleman/gg
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
	asteroids []Asteroid
	player    Player
}

// ------------------------------------------------------------------------
func (g *Game) Init() {
	g.Done = false
	g.player = MakePlayer()
	g.level = 1
	g.makeLevel()
	//g.removeAsteroid(1)
}

// ------------------------------------------------------------------------
func (g *Game) Update() error {
	if ebiten.IsKeyPressed(ebiten.KeyEscape) {
		g.Done = true
	}

	for i := range g.asteroids {
		g.asteroids[i].Update(MAX_X, MAX_Y)
	}
	g.player.Update(MAX_X, MAX_Y)

	if ebiten.IsKeyPressed(ebiten.KeyD) {
		g.Debug = !g.Debug
	}

	return nil
}

// ------------------------------------------------------------------------
func (g *Game) Draw(screen *ebiten.Image) {
	g.player.Draw(screen)
	for i := range g.asteroids {
		g.asteroids[i].Draw(screen)
	}
	if g.Debug {
		g.DrawDebug(screen)
	}
}

// ------------------------------------------------------------------------
func (g *Game) DrawDebug(screen *ebiten.Image) {

	msg := fmt.Sprintf("FPS: %.1f\nTPS: %.1f", ebiten.ActualFPS(), ebiten.ActualTPS())
	ebitenutil.DebugPrint(screen, msg)

	msg2 := fmt.Sprintf("Player: %v", g.player)
	ebitenutil.DebugPrintAt(screen, msg2, 0, 50)

	for i, v := range g.asteroids {
		msg := fmt.Sprintf("%d: %v", i, v)
		ebitenutil.DebugPrintAt(screen, msg, 0, 80+(i*18))
	}
}

// ------------------------------------------------------------------------
func (g *Game) Layout(outsideWidth, outsideHeight int) (screenWidth, screenHeight int) {
	return MAX_X, MAX_Y
}

// ------------------------------------------------------------------------
func (g *Game) removeAsteroid(index int) {
	g.asteroids = append(g.asteroids[:index], g.asteroids[index+1:]...)
}

// ------------------------------------------------------------------------
func (g *Game) addAsteroid(a Asteroid) {
	g.asteroids = append(g.asteroids, a)
}

// ------------------------------------------------------------------------
func (g *Game) makeLevel() {
	//num := (g.level-1)/2 + 1
	//stage := 3 - (g.level % 2)
	num := 5
	for i := 0; i < num; i++ {
		dir := getRandDirection()
		spd := getRandSpeed()
		x := float64(rand.Intn(MAX_X))
		y := float64(rand.Intn(MAX_Y))
		g.addAsteroid(MakeAsteroid(x, y, dir, spd))
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
