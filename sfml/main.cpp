#include <iostream>
#include <map>
#include <cmath>
#include <SFML/Graphics.hpp>

using namespace std;

const int MAX_X = 1024;
const int MAX_Y = 768;
const int FPS = 30;


//------------------------------------------------------------------------
class GameObject
{
	public:

		float pos_x, pos_y;
		float vel_x, vel_y;
		float angle;

		GameObject(float x, float y, float a=0, float dx=0, float dy=0)
		{
			pos_x = x;
			pos_y = y;
			vel_x = dx;
			vel_y = dy;
			angle = a;
		}

		void update()
		{
			pos_x += vel_x;
			pos_y += vel_y;
			check_boundry();
		}

	protected:

		void check_boundry()
		{
			if (pos_x > MAX_X)  pos_x = pos_x - MAX_X;
			if (pos_x < 0)      pos_x = MAX_X - pos_x;

			if (pos_y > MAX_Y)  pos_y = pos_y - MAX_Y;
			if (pos_y < 0)      pos_y = MAX_Y - pos_y;

			angle = (int) angle % 360;
		}

};

//------------------------------------------------------------------------
class Player : public GameObject, public sf::ConvexShape
{
	public:
		Player() : GameObject(MAX_X/2.0, MAX_Y/2.0, -90), sf::ConvexShape()
		{
			setPointCount(3);
			setPoint(0, sf::Vector2f(20, 0));
			setPoint(1, sf::Vector2f(-10, 10));
			setPoint(2, sf::Vector2f(-10, -10));
			setFillColor(sf::Color::Black);
			setOutlineColor(sf::Color::White);
			setOutlineThickness(2.0f);
			setOrigin(0, 0);
		}

		void update(map<string, int> &ctrl)
		{
			angle += (ctrl["right"] - ctrl["left"]) * 8.f;
			if (ctrl["thrust"])
			{
				vel_x += cos(angle * M_PI / 180.0) * 0.5;
				vel_y += sin(angle * M_PI / 180.0) * 0.5;
			}

			GameObject::update();

			// prep for draw
			setRotation(angle);
			setPosition(pos_x, pos_y);
		}

};



/*****************************************************/
int main()
{
	sf::RenderWindow window(sf::VideoMode(MAX_X, MAX_Y), "Classic Asteroids");
	window.setFramerateLimit(FPS);

	map<string, int> controls;
	controls["quit"] = 0;
	controls["left"] = 0;
	controls["right"] = 0;
	controls["thrust"] = 0;
	controls["fire"] = 0;

	Player player;
	sf::Event event;
	sf::Clock clock;

	// main game loop
	while (window.isOpen() && !controls["quit"])
	{
		// handle events and update the user controls
		while (window.pollEvent(event))
		{
			switch (event.type)
			{
				case sf::Event::Closed:
					window.close();
					break;

				case sf::Event::KeyPressed:

					switch(event.key.code)
					{
						case sf::Keyboard::Escape:  controls["quit"] = 1; break;
						case sf::Keyboard::Left:    controls["left"] = 1; break;
						case sf::Keyboard::Right:   controls["right"] = 1; break;
						case sf::Keyboard::Up:      controls["thrust"] = 1; break;
						default:
							break;
					}
					break;

				case sf::Event::KeyReleased:
					switch(event.key.code)
					{
						case sf::Keyboard::Escape:  controls["quit"] = 0; break;
						case sf::Keyboard::Left:    controls["left"] = 0; break;
						case sf::Keyboard::Right:   controls["right"] = 0; break;
						case sf::Keyboard::Up:      controls["thrust"] = 0; break;
						default:
							break;
					}
					break;

				default:
					break;
			}

		}

		// update the game world
		//sf::Time elapsed = clock.restart();
		//player.update(controls, elapsed.asSeconds());
		player.update(controls);

		// render
		window.clear();
		window.draw(player);
		window.display();
	}

	return 0;
}

