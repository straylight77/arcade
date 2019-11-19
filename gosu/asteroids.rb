require 'gosu'

module ZOrder
  BACKGROUND, STARS, PLAYER, UI = *0..3
end

# -----------------------------------------------------------------------
class GameObject
  def initialize(anim=nil, pos_x=nil, pos_y=nil, vel_x=nil, vel_y=nil)
    @x = @y = @vel_x = @vel_y = @angle = 0.0
  end

  def set_position(x, y)
    @x, @y = x, y
  end

  def set_velocity(vel_x, vel_y)
    @vel_x, @vel_y = vel_x, vel_y
  end

  def move
    @x += @vel_x
    @y += @vel_y
    @x %= 800
    @y %= 600
  end
end

# -----------------------------------------------------------------------
class Player < GameObject
  def initialize
    super
    @image = Gosu::Image.new("media/ship1_32x32.png")
    @score = 0
  end

  def turn_left
    @angle -= 4.5
  end

  def turn_right
    @angle += 4.5
  end

  def accelerate
    @vel_x += Gosu.offset_x(@angle, 0.5)
    @vel_y += Gosu.offset_y(@angle, 0.5)
  end

  def move
    super
    @vel_x *= 0.95
    @vel_y *= 0.95
  end

  def draw
    @image.draw_rot(@x, @y, 1, @angle)
  end

end

# -----------------------------------------------------------------------
class Asteroid < GameObject
  attr_reader :x, :y

  def initialize(animation, pos_x=nil, pos_y=nil, vel_x=nil, vel_y=nil)
    super
    @animation = animation
    @x = pos_x.nil? ? rand * 800 : pos_x
    @y = pos_y.nil? ? rand * 800 : pos_y
    @vel_x = vel_x.nil? ? 0.5 : vel_x
    @vel_y = vel_y.nil? ? 1.0 : vel_y

  end

  def draw
    img = @animation[Gosu.milliseconds / 100 % @animation.size]
    x = @x - img.width / 2.0
    y = @y - img.height / 2.0
    img.draw(x, y, ZOrder::STARS, 1, 1)
  end
end

# -----------------------------------------------------------------------
class Game < Gosu::Window
  def initialize
    super 800, 600
    self.caption = "Asteroids!"
    #@background_image = Gosu::Image.new("media/space.png", :tileable => true)

    @player = Player.new
    @player.set_position(400, 300)

    @asteroid_anim = Gosu::Image.load_tiles("media/asteroid2.png", 64, 64)
    @asteroids = Array.new
    @asteroids.push( Asteroid.new(@asteroid_anim) )
  end


  def handle_input
    if Gosu.button_down? Gosu::KB_LEFT or Gosu::button_down? Gosu::GP_LEFT
      @player.turn_left
    end
    if Gosu.button_down? Gosu::KB_RIGHT or Gosu::button_down? Gosu::GP_RIGHT
      @player.turn_right
    end
    if Gosu.button_down? Gosu::KB_UP or Gosu::button_down? Gosu::GP_BUTTON_0
      @player.accelerate
    end
    if Gosu.button_down? Gosu::KB_N
      @asteroids.push( Asteroid.new(@asteroid_anim) )
    end
  end

  def update
    handle_input
    @player.move
    @asteroids.each { |ast| ast.move }
  end

  def draw
    @player.draw
    @asteroids.each { |ast| ast.draw }
    #@background_image.draw(0, 0, 0)
  end

  # helper functions
  def button_down(id)
    if id == Gosu::KB_ESCAPE
      close
    else
      super
    end
  end

end


Game.new.show
