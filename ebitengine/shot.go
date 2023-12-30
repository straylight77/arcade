package main

import (
	"fmt"
	"math"
)

type Shot struct {
	GameObject
	timeToLive int
	dead       bool
}

// ------------------------------------------------------------------------
func MakeShot(x, y, direction, speed float64) *Shot {
	vx := math.Cos(direction*math.Pi/180) * speed
	vy := math.Sin(direction*math.Pi/180) * speed
	s := &Shot{
		GameObject{X: x, Y: y, VelX: vx, VelY: vy},
		60 * 1, // 1 sec
		false,
	}
	s.LoadSprite("laserBlue02.png")
	return s
}

func MakeShotFromPlayer(p *Player) *Shot {
	s := MakeShot(
		p.X,
		p.Y,
		p.Angle,
		p.Speed()+10.0,
	)
	s.Angle = p.Angle + 90.0 // remove this after updating the sprite image
	return s
}

// ------------------------------------------------------------------------
func (s *Shot) Update(maxX, maxY float64) {
	s.UpdatePosition(maxX, maxY)
	if s.timeToLive > 0 {
		s.timeToLive--
	}
	if s.timeToLive <= 0 {
		s.dead = true
	}
}

// ------------------------------------------------------------------------
func (s *Shot) IsDead() bool {
	return s.dead
}

// ------------------------------------------------------------------------
func (s Shot) String() string {
	return fmt.Sprintf(
		"[%.1f, %.1f] (%.1f, %.1f) %v %v",
		s.VelX, s.VelY,
		s.X, s.Y,
		s.timeToLive,
		s.dead,
	)
}
