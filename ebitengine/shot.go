package main

import (
	"fmt"
	"math"

	"github.com/hajimehoshi/ebiten/v2"
)

var ShotImg *ebiten.Image

func init() {
	ShotImg = MustLoadImage("assets/laserBlue02.png")
}

/**************************************************************************
 *                                Shot                                    *
 **************************************************************************/
type Shot struct {
	GameObject
	timeToLive int
	Dead       bool
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
	//s.LoadSprite("laserBlue02.png")
	s.Img = ShotImg
	size := s.Img.Bounds().Size()
	s.Width = float64(size.X)
	s.Height = float64(size.Y)
	s.Radius = 10

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
		s.Dead = true
	}
}

// ------------------------------------------------------------------------
func (s *Shot) IsDead() bool {
	return s.Dead
}

// ------------------------------------------------------------------------
func (s *Shot) Kill() {
	s.Dead = true
}

// ------------------------------------------------------------------------
func (s Shot) String() string {
	return fmt.Sprintf(
		"[%.1f, %.1f] (%.1f, %.1f) %v %v",
		s.VelX, s.VelY,
		s.X, s.Y,
		s.timeToLive,
		s.Dead,
	)
}
