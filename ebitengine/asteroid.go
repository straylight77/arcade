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
	Stage int
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
	return MakeAsteroid(3, 250, 250, 45, 3)
}

// ------------------------------------------------------------------------
func MakeAsteroid(stage int, x, y, direction, speed float64) *Asteroid {
	vx := math.Cos(direction*math.Pi/180) * speed
	vy := math.Sin(direction*math.Pi/180) * speed
	a := &Asteroid{
		GameObject{X: x, Y: y, VelX: vx, VelY: vy},
		stage,
	}

	//a.Img = AsteroidImg
	switch stage {
	case 3:
		a.LoadSprite("meteorBrown_big1.png")
	case 2:
		a.LoadSprite("meteorBrown_med1.png")
	case 1:
		a.LoadSprite("meteorBrown_small1.png")
	default:
		a.LoadSprite("meteorGrey_big1.png")
	}

	size := a.Img.Bounds().Size()
	a.Width = float64(size.X)
	a.Height = float64(size.Y)
	a.Radius = math.Min(a.Width, a.Height) * 0.75

	return a
}

// ------------------------------------------------------------------------
func (a *Asteroid) Split() (*Asteroid, *Asteroid) {
	dir := a.Direction()
	spd := a.Speed()
	stg := a.Stage - 1
	var new_a1, new_a2 *Asteroid
	new_a1 = MakeAsteroid(stg, a.X, a.Y, dir-65.0, spd)
	new_a2 = MakeAsteroid(stg, a.X, a.Y, dir+65.0, spd)
	return new_a1, new_a2
}
