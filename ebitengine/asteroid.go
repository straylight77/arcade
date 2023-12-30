package main

import (
	"math"
	"math/rand"

	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/ebitenutil"
)

var AsteroidImg *ebiten.Image

func init() {
	fname := "meteorBrown_big1.png"
	var err error
	AsteroidImg, _, err = ebitenutil.NewImageFromFile(fname)
	if err != nil {
		panic(err)
	}
}

/**************************************************************************
 *                               Asteroid                                 *
 **************************************************************************/
type Asteroid struct {
	GameObject
	stage int
}

// ------------------------------------------------------------------------
func getRandDirection() float64 {
	return rand.Float64() * 360
}

// ------------------------------------------------------------------------
func getRandSpeed() float64 {
	return rand.Float64()*(4-2) + 2
}

// ------------------------------------------------------------------------
func MakeRandomAsteroid() *Asteroid {
	return MakeAsteroid(250, 250, 45, 3)
}

// ------------------------------------------------------------------------
func MakeAsteroid(x, y, direction, speed float64) *Asteroid {
	vx := math.Cos(direction*math.Pi/180) * speed
	vy := math.Sin(direction*math.Pi/180) * speed
	a := &Asteroid{
		GameObject{X: x, Y: y, VelX: vx, VelY: vy},
		3,
	}

	//a.LoadSprite("meteorBrown_big1.png")
	a.Img = AsteroidImg
	size := a.Img.Bounds().Size()
	a.Width = float64(size.X)
	a.Height = float64(size.Y)
	a.Radius = math.Min(a.Width, a.Height) * 0.75

	return a
}
