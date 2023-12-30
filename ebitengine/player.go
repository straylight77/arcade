package main

import (
	"fmt"
	"math"
)

/**************************************************************************
 *                                 Player                                 *
 **************************************************************************/
type Player struct {
	GameObject
}

// ------------------------------------------------------------------------
func MakePlayer() Player {
	p := Player{
		GameObject{X: MAX_X / 2, Y: MAX_Y / 2, VelX: 0, VelY: 0, Angle: -90},
	}
	p.LoadSprite("playerShip1_blue.png")
	return p
}

// ------------------------------------------------------------------------
func (p Player) String() string {
	return fmt.Sprintf(
		"%.1f [%.1f, %.1f] (%.1f, %.1f)",
		p.Angle,
		p.VelX, p.VelY,
		p.X, p.Y,
	)
}

// ------------------------------------------------------------------------
func (p *Player) Update(maxX, maxY float64, ctrl Controls) {

	rotateSpeed := 200.0
	thrust := 0.1

	turn := ctrl.Cmd["right"] - ctrl.Cmd["left"]
	p.Angle += float64(turn) * rotateSpeed * 2 * math.Pi / 360

	if ctrl.Cmd["thrust"] == 1 {
		p.VelX += math.Cos(p.Angle*math.Pi/180) * thrust
		p.VelY += math.Sin(p.Angle*math.Pi/180) * thrust
	}

	p.X += p.VelX
	p.Y += p.VelY
	p.checkBoundary(maxX, maxY)
}
