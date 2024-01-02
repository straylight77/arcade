package main

import (
	"fmt"
	"math"

	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/ebitenutil"
)

type Sprite interface {
	GetPos() (float64, float64)
	GetRadius() float64
	//Speed() float64
	//Direction() float64
	//Update(float64, float64)
	Draw(*ebiten.Image)
	IsDead() bool
	IntersectsWith(Sprite) bool
}

/**************************************************************************
 *                              GameObject                                *
 **************************************************************************/
type GameObject struct {
	X, Y          float64
	Angle         float64
	VelX, VelY    float64
	Img           *ebiten.Image
	Width, Height float64
	Radius        float64
}

// ------------------------------------------------------------------------
func (obj *GameObject) Update(maxX, maxY float64) {
	obj.UpdatePosition(maxX, maxY)
}

// ------------------------------------------------------------------------
func (obj *GameObject) Draw(screen *ebiten.Image) {
	op := &ebiten.DrawImageOptions{}
	op.GeoM.Translate(-obj.Width/2, -obj.Height/2)
	//op.GeoM.Scale(0.5, 0.5)
	op.GeoM.Rotate(obj.Angle * 2 * math.Pi / 360)
	op.GeoM.Translate(obj.X, obj.Y)
	screen.DrawImage(obj.Img, op)
}

// ------------------------------------------------------------------------
func (obj *GameObject) IsDead() bool {
	return false
}

// ------------------------------------------------------------------------
func (obj *GameObject) Speed() float64 {
	return math.Sqrt(obj.VelX*obj.VelX + obj.VelY*obj.VelY)
}

// ------------------------------------------------------------------------
func (obj *GameObject) Direction() float64 {
	return math.Atan2(obj.VelY, obj.VelX) * 180.0 / math.Pi
}

// ------------------------------------------------------------------------
func (obj *GameObject) GetPos() (float64, float64) {
	return obj.X, obj.Y
}

// ------------------------------------------------------------------------
func (obj *GameObject) GetRadius() float64 {
	return obj.Radius
}

// ------------------------------------------------------------------------
func (obj *GameObject) IntersectsWith(obj2 Sprite) bool {
	x1, y1 := obj.GetPos()
	x2, y2 := obj2.GetPos()
	dx := x2 - x1
	dy := y2 - y1
	dist := math.Sqrt(dx*dx + dy*dy)
	intersects := dist < (obj2.GetRadius() + obj.GetRadius())
	return intersects
}

// ------------------------------------------------------------------------
func (obj *GameObject) UpdatePosition(maxX, maxY float64) {
	obj.X += obj.VelX
	obj.Y += obj.VelY
	obj.checkBoundary(maxX, maxY)
}

// ------------------------------------------------------------------------
func (obj *GameObject) checkBoundary(maxX, maxY float64) {
	hpad := obj.Width / 2
	vpad := obj.Height / 2

	if obj.X+hpad < 0 { // left side
		obj.X = maxX + hpad
	} else if obj.X-hpad > maxX { // right side
		obj.X = -hpad
	}

	if obj.Y+vpad < 0 { // top
		obj.Y = maxY + vpad
	} else if obj.Y-vpad > maxY { // bottom
		obj.Y = -vpad
	}

	//obj.Angle = float64(int(obj.Angle) % 360)
}

// ------------------------------------------------------------------------
func (obj *GameObject) LoadSprite(fname string) {
	var err error
	obj.Img, _, err = ebitenutil.NewImageFromFile(fname)
	if err != nil {
		panic(err)
	}
	size := obj.Img.Bounds().Size()
	obj.Width = float64(size.X)
	obj.Height = float64(size.Y)
	obj.Radius = math.Min(obj.Width, obj.Height) * 0.6
}

// ------------------------------------------------------------------------
func (obj GameObject) String() string {
	return fmt.Sprintf(
		"[%.1f, %.1f] (%.1f, %.1f)",
		obj.VelX, obj.VelY,
		obj.X, obj.Y,
	)
}
