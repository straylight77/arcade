package main

import (
	"math"
	"math/rand"
)

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
	a.LoadSprite("meteorBrown_big1.png")
	return a
}
