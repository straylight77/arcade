package main

import (
	"fmt"
	"math"

	"github.com/hajimehoshi/ebiten/v2"
)

/**************************************************************************
 *                                 Player                                 *
 **************************************************************************/
type Player struct {
	GameObject
	Invincible int
}

// ------------------------------------------------------------------------
func MakePlayer() *Player {
	p := &Player{}
	p.LoadSprite("assets/playerShip1_blue.png")
	p.Reset()
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

	if p.Invincible > 0 {
		p.Invincible--
	}
}

// ------------------------------------------------------------------------
func (obj *Player) Draw(screen *ebiten.Image) {
	if obj.Invincible%16 < 8 {
		op := &ebiten.DrawImageOptions{}
		op.GeoM.Translate(-obj.Width/2, -obj.Height/2)
		op.GeoM.Rotate(obj.Angle * 2 * math.Pi / 360)
		op.GeoM.Translate(obj.X, obj.Y)
		screen.DrawImage(obj.Img, op)
	}
}

// ------------------------------------------------------------------------
func (p *Player) Reset() {
	p.X = MAX_X / 2
	p.Y = MAX_Y / 2
	p.VelX = 0
	p.VelY = 0
	p.Angle = -90
	p.Invincible = 60 * 3
}
