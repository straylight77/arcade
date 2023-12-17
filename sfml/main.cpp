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
class Player : public sf::ConvexShape
{
	public:

		sf::Vector2f vel;

		Player(sf::Vector2f p, float a, sf::Vector2f v) :
			vel(v)
		{
			setPointCount(3);
			setPoint(0, sf::Vector2f(20, 0));
			setPoint(1, sf::Vector2f(-10, 10));
			setPoint(2, sf::Vector2f(-10, -10));
			setFillColor(sf::Color::Black);
			setOutlineColor(sf::Color::White);
			setOutlineThickness(2.0f);
			setOrigin(0, 0);
			setPosition(p);
			setRotation(-90.0);
		}

		void update(map<string, int> &ctrl)
		{
			rotate( (ctrl["right"] - ctrl["left"]) * 8.0);
			float angle = getRotation();

			if (ctrl["thrust"])
			{
				vel.x += cos(angle * M_PI / 180.0) * 0.5;
				vel.y += sin(angle * M_PI / 180.0) * 0.5;
			}
			move(vel);
			check_boundary(10);
		}

	private:

		void check_boundary(float padding)
		{
			sf::Vector2f pos = getPosition();

			if (pos.x + padding < 0)           pos.x = MAX_X + padding;    // left side
			else if (pos.x - padding > MAX_X)  pos.x = -padding;	       // right side

			if (pos.y + padding < 0)           pos.y = MAX_Y + padding;    // top
			else if (pos.y - padding > MAX_Y)  pos.y = -padding;           // bottom

			setPosition(pos);
		}

};


//------------------------------------------------------------------------
class Asteroid : public sf::ConvexShape
{
	public:

		sf::Vector2f vel;

		Asteroid(float r, sf::Vector2f p, sf::Vector2f v) :
			vel(v)
		{
			setPointCount(10);
			setPoint(0, sf::Vector2f(60, -20));
			setPoint(1, sf::Vector2f(40, -40));
			setPoint(2, sf::Vector2f(20, -60));
			setPoint(3, sf::Vector2f(-20, -60));
			setPoint(4, sf::Vector2f(-40, -40));
			setPoint(5, sf::Vector2f(-60, -20));
			setPoint(6, sf::Vector2f(-60, 20));
			setPoint(7, sf::Vector2f(-40, 40));
			setPoint(8, sf::Vector2f(-20, 60));
			setPoint(9, sf::Vector2f(20, 60));
			setFillColor(sf::Color::Black);
			setOutlineThickness(3.0);
			setOrigin(r, r);
			setPosition(p);
		}

		void update()
		{
			move(vel);
			check_boundary();
		}

	private:

		void check_boundary()
		{
			sf::Vector2f pos = getPosition();
			float r = 120;

			if (pos.x + r < 0)          pos.x = MAX_X + r;    // left side
			else if (pos.x -r > MAX_X)  pos.x = -r;	          // right side

			if (pos.y + r < 0)          pos.y = MAX_Y + r;    // top
			else if (pos.y -r > MAX_Y)  pos.y = -r;           // bottom

			setPosition(pos);
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
			window.draw(a);
		}
		window.draw(player);
		window.display();
	}

	return 0;
}

