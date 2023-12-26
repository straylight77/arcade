package main

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
	level     int
	asteroids []Asteroid
}

// ------------------------------------------------------------------------
func (g *Game) Init() {
	g.level = 1
	g.makeLevel()
	//g.removeAsteroid(1)
}

// ------------------------------------------------------------------------
func (g *Game) Update() error {
	for i := range g.asteroids {
		g.asteroids[i].Update(MAX_X, MAX_Y)
	}
	return nil
}

// ------------------------------------------------------------------------
func (g *Game) Draw(screen *ebiten.Image) {
	for i := range g.asteroids {
		g.asteroids[i].Draw(screen)
	}
	g.DrawDebug(screen)
}

// ------------------------------------------------------------------------
func (g *Game) DrawDebug(screen *ebiten.Image) {
	msg := fmt.Sprintf(
		"FPS: %.1f\nAsteroids: %d",
		ebiten.ActualFPS(),
		len(g.asteroids),
	)
	ebitenutil.DebugPrint(screen, msg)

	for i, v := range g.asteroids {
		msg := fmt.Sprintf(
			"%d: (%3.1f, %3.1f) / (%3.1f, %3.1f)",
			i,
			v.X, v.Y,
			v.VelX, v.VelY,
		)
		ebitenutil.DebugPrintAt(screen, msg, 0, 50+(i*18))
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
