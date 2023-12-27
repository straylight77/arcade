package main

import (
	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/inpututil"
)

type Controls struct {
	keysUp   []ebiten.Key
	keysDown []ebiten.Key
	Cmd      map[string]int
}

func (ctrl *Controls) Init() {
	ctrl.Cmd = make(map[string]int)
}

func (ctrl *Controls) mapKeyToCommand(key ebiten.Key) string {

	var cmd_str string

	switch key {
	case ebiten.KeyD:
		cmd_str = "debug"
	case ebiten.KeyLeft:
		cmd_str = "left"
	case ebiten.KeyRight:
		cmd_str = "right"
	case ebiten.KeyUp:
		cmd_str = "thrust"
	case ebiten.KeyControl:
		cmd_str = "fire"
	case ebiten.KeyEscape:
		cmd_str = "quit"
	default:
		cmd_str = "unknown"
		//fmt.Printf("%T: %v", k, k)
		//panic(0)
	}
	return cmd_str
}

func (ctrl *Controls) handleInput() {

	ctrl.keysUp = inpututil.AppendJustPressedKeys(ctrl.keysUp[:0])
	for _, k := range ctrl.keysUp {
		cmd_str := ctrl.mapKeyToCommand(k)
		ctrl.Cmd[cmd_str] = 1
	}

	ctrl.keysDown = inpututil.AppendJustReleasedKeys(ctrl.keysDown[:0])
	for _, k := range ctrl.keysDown {
		cmd_str := ctrl.mapKeyToCommand(k)
		ctrl.Cmd[cmd_str] = 0
	}

}
