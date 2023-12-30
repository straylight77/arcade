package main

import "github.com/hajimehoshi/ebiten/v2"

type Sprite interface {
	Draw(*ebiten.Image)
	Update(float64, float64)
}

type SpriteGroup struct {
	sprites []Sprite
}

func (g *SpriteGroup) Add(s Sprite) {
	g.sprites = append(g.sprites, s)
}

func (g *SpriteGroup) Remove(idx int) {
	g.sprites = append(g.sprites[:idx], g.sprites[idx+1:]...)
}

func (g *SpriteGroup) GetSprites() []Sprite {
	return g.sprites
}

func (g *SpriteGroup) Draw(screen *ebiten.Image) {
	for i := range g.sprites {
		g.sprites[i].Draw(screen)
	}
}

func (g *SpriteGroup) Update(maxX, maxY float64) {
	for i := range g.sprites {
		g.sprites[i].Update(maxX, maxY)
	}
}
