#include <iostream>
#include <map>
#include <cmath>
#include <SFML/Graphics.hpp>

using namespace std;

const int MAX_X = 1024;
const int MAX_Y = 768;
const int FPS = 30;


//------------------------------------------------------------------------
class GameControls
{
	public:

		GameControls()
		{
			controls["quit"] = 0;
			controls["left"] = 0;
			controls["right"] = 0;
			controls["thrust"] = 0;
			controls["fire"] = 0;
		}

		int getState(string cmd)
		{
			return controls[cmd];
		}

		void setState(string cmd, int val)
		{
			controls[cmd] = val;
		}

		string mapKeyToControl(sf::Keyboard::Key key)
		{
			switch(key)
			{
				case sf::Keyboard::Escape:  return "quit"; break;
				case sf::Keyboard::Left:    return "left"; break;
				case sf::Keyboard::Right:   return "right"; break;
				case sf::Keyboard::Up:      return "thrust"; break;
				default:					return "unknown"; break;
			}
		}

		void handleEvent(sf::Event event)
		{
			string cmd;
			switch (event.type)
			{
				case sf::Event::Closed:
					//window.close();
					controls["quit"] = 1;
					break;

				case sf::Event::KeyPressed:
					cmd = mapKeyToControl(event.key.code);
					setState(cmd, 1);
					break;

				case sf::Event::KeyReleased:
					cmd = mapKeyToControl(event.key.code);
					setState(cmd, 0);
					break;

				default:
					break;
			}
		}

	private:
		map<string, int> controls;
};


//------------------------------------------------------------------------
class GameObject
{
	public:

		sf::ConvexShape shape;
		sf::Vector2f vel;

		GameObject(sf::Vector2f p, float a, sf::Vector2f v) :
			shape(),
			vel(v)
		{
			shape.setPosition(p);
			shape.setRotation(a);
		}

	protected:

		void checkBoundary(float padding)
		{
			sf::Vector2f pos = shape.getPosition();

			if (pos.x + padding < 0)           pos.x = MAX_X + padding;    // left side
			else if (pos.x - padding > MAX_X)  pos.x = -padding;	       // right side

			if (pos.y + padding < 0)           pos.y = MAX_Y + padding;    // top
			else if (pos.y - padding > MAX_Y)  pos.y = -padding;           // bottom

			shape.setPosition(pos);
		}
};


//------------------------------------------------------------------------
class Player : public GameObject
{
	public:

		Player(sf::Vector2f p, float a, sf::Vector2f v) :
			GameObject(p, a, v)
		{
			shape.setPointCount(3);
			shape.setPoint(0, sf::Vector2f(20, 0));
			shape.setPoint(1, sf::Vector2f(-10, 10));
			shape.setPoint(2, sf::Vector2f(-10, -10));
			shape.setFillColor(sf::Color::Black);
			shape.setOutlineColor(sf::Color::White);
			shape.setOutlineThickness(2.0f);
			shape.setOrigin(0, 0);
		}

		void update(GameControls &ctrl)
		{
			shape.rotate( (ctrl.getState("right") - ctrl.getState("left")) * 8.0);
			float angle = shape.getRotation();

			if (ctrl.getState("thrust"))
			{
				vel.x += cos(angle * M_PI / 180.0) * 0.5;
				vel.y += sin(angle * M_PI / 180.0) * 0.5;
			}
			shape.move(vel);
			checkBoundary(10);
		}
};


//------------------------------------------------------------------------
class Asteroid : public GameObject
{
	public:

		Asteroid(float r, sf::Vector2f p, sf::Vector2f v) :
			GameObject(p, 0, v)
		{
			shape.setPointCount(10);
			shape.setPoint(0, sf::Vector2f(60, -20));
			shape.setPoint(1, sf::Vector2f(40, -40));
			shape.setPoint(2, sf::Vector2f(20, -60));
			shape.setPoint(3, sf::Vector2f(-20, -60));
			shape.setPoint(4, sf::Vector2f(-40, -40));
			shape.setPoint(5, sf::Vector2f(-60, -20));
			shape.setPoint(6, sf::Vector2f(-60, 20));
			shape.setPoint(7, sf::Vector2f(-40, 40));
			shape.setPoint(8, sf::Vector2f(-20, 60));
			shape.setPoint(9, sf::Vector2f(20, 60));
			shape.setFillColor(sf::Color::Black);
			shape.setOutlineThickness(3.0);
			shape.setOrigin(r, r);
		}

		void update()
		{
			shape.move(vel);
			checkBoundary(120);
		}
};


/*****************************************************/
int main()
{
	sf::RenderWindow window(sf::VideoMode(MAX_X, MAX_Y), "Classic Asteroids");
	window.setFramerateLimit(FPS);

	GameControls controls;

	// initialize game objects
	Player player(sf::Vector2f(MAX_X/2, MAX_Y/2), -90, sf::Vector2f(0, 0));
	vector<Asteroid> asteroids;
	asteroids.emplace_back(60, sf::Vector2f(200, 250), sf::Vector2f(0, -5));
	asteroids.emplace_back(60, sf::Vector2f(200, 400), sf::Vector2f(5, 0));

	sf::Event event;
	sf::Clock clock;

	// main game loop
	while (window.isOpen() && !controls.getState("quit"))
	{
		// handle events and update the user controls
		while (window.pollEvent(event))
		{
			controls.handleEvent(event);

			if (controls.getState("quit"))
				window.close();
		}

		// update the game world
		for (auto& a : asteroids)
			a.update();
		player.update(controls);

		// render
		window.clear();
		for (auto& a : asteroids)
			window.draw(a.shape);
		window.draw(player.shape);
		window.display();
	}

	return 0;
}

