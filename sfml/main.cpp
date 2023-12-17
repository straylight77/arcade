#include <iostream>
#include <map>
#include <list>
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

		void update(map<string, int> &ctrl)
		{
			shape.rotate( (ctrl["right"] - ctrl["left"]) * 8.0);
			float angle = shape.getRotation();

			if (ctrl["thrust"])
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

	map<string, int> controls;
	controls["quit"] = 0;
	controls["left"] = 0;
	controls["right"] = 0;
	controls["thrust"] = 0;
	controls["fire"] = 0;

	Player player(sf::Vector2f(MAX_X/2, MAX_Y/2), -90, sf::Vector2f(0, 0));

	vector<Asteroid> asteroids;
	asteroids.emplace_back(60, sf::Vector2f(200, 250), sf::Vector2f(0, -5));
	asteroids.emplace_back(60, sf::Vector2f(200, 400), sf::Vector2f(5, 0));


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
		player.update(controls);
		for (auto& a : asteroids)
		{
			a.update();
		}

		// render
		window.clear();
		for (auto& a : asteroids)
		{
			window.draw(a.shape);
		}
		window.draw(player.shape);
		window.display();
	}

	return 0;
}

