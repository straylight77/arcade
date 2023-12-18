#include <iostream>
#include <memory>
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
				case sf::Keyboard::Escape:		return "quit"; break;
				case sf::Keyboard::Left:		return "left"; break;
				case sf::Keyboard::Right:		return "right"; break;
				case sf::Keyboard::Up:			return "thrust"; break;
				case sf::Keyboard::LControl:	return "fire"; break;
				default:						return "unknown"; break;
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

		GameObject(sf::Vector2f p, sf::Vector2f v)
		{
			shape.setPosition(p);
			vel = v;
		}

		GameObject(sf::Vector2f p, float angle, float speed)
		{
			shape.setPosition(p);
			float x = cos(angle * M_PI / 180.0) * speed;
			float y = sin(angle * M_PI / 180.0) * speed;
			vel = sf::Vector2f(x, y);
		}

		sf::Vector2f getPos()
		{
			return shape.getPosition();
		}

		float getAngle()
		{
			return shape.getRotation();
		}

		void update()
		{
			shape.move(vel);
			checkBoundary();
		}

		sf::FloatRect getHitbox()
		{
			return shape.getGlobalBounds();
		}

	protected:

		void checkBoundary()
		{
			sf::Vector2f pos = shape.getPosition();
			int width = shape.getGlobalBounds().width;
			int height = shape.getGlobalBounds().height;

			if (pos.x + width < 0)           pos.x = MAX_X + width;    // left side
			else if (pos.x - width > MAX_X)  pos.x = -width;	       // right side

			if (pos.y + height < 0)           pos.y = MAX_Y + height;    // top
			else if (pos.y - height > MAX_Y)  pos.y = -height;           // bottom

			shape.setPosition(pos);
		}
};


//------------------------------------------------------------------------
class Player : public GameObject
{
	public:

		Player(sf::Vector2f p, sf::Vector2f v) :
			GameObject(p, v)
		{
			shape.setPointCount(3);
			shape.setPoint(0, sf::Vector2f(20, 0));
			shape.setPoint(1, sf::Vector2f(-10, 10));
			shape.setPoint(2, sf::Vector2f(-10, -10));
			shape.setFillColor(sf::Color::Black);
			shape.setOutlineColor(sf::Color::White);
			shape.setOutlineThickness(2.0f);
			shape.setOrigin(0, 0);

			shape.setRotation(-90);
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
			GameObject::update();
		}
};


//------------------------------------------------------------------------
class Asteroid : public GameObject
{
	public:

		Asteroid(float r, sf::Vector2f p, sf::Vector2f v) :
			GameObject(p, v)
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

};


//------------------------------------------------------------------------
class Shot : public GameObject
{
	public:
		bool is_done;
		int time_to_live; // in frames

		Shot(sf::Vector2f p, float angle, float speed = 20.f) :
			GameObject(p, angle, speed)
		{
			shape.setPointCount(4);
			shape.setPoint(0, sf::Vector2f(-2.5, -2.5));
			shape.setPoint(1, sf::Vector2f(-2.5, 2.5));
			shape.setPoint(2, sf::Vector2f(2.5, 2.5));
			shape.setPoint(3, sf::Vector2f(2.5, -2.5));
			shape.setOrigin(0, 0);
			is_done = false;
			time_to_live = FPS;  // FPS * seconds of real-time
		}

		void update()
		{
			//GameObject::update();
			shape.move(vel);
			time_to_live--;
		}


};



/*****************************************************/
int main()
{
	sf::RenderWindow window(sf::VideoMode(MAX_X, MAX_Y), "Classic Asteroids");
	window.setFramerateLimit(FPS);

	GameControls controls;

	// initialize game objects
	Player player(sf::Vector2f(MAX_X/2, MAX_Y/2), sf::Vector2f(0, 0));
	vector<std::shared_ptr<Shot>> shots;

	vector<Asteroid> asteroids;
	asteroids.emplace_back(60, sf::Vector2f(200, 250), sf::Vector2f(0, -5));
	asteroids.emplace_back(60, sf::Vector2f(200, 400), sf::Vector2f(5, 0));


	sf::Event event;
	sf::Clock clock;

	sf::FloatRect player_box, a_box;

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

		for (auto s = shots.begin(); s != shots.end(); /* no increment here */)
		{
			(*s)->update();

			if ((*s)->time_to_live <= 0) {
				s = shots.erase(s); // Efficient removal using iterator
			} else {
				++s;
			}
		}

		player.update(controls);

		if (controls.getState("fire"))
		{
			if (shots.size() < 3) // limit number of active shots
			{
				shots.push_back(std::make_shared<Shot>( player.getPos(), player.getAngle() ));
				controls.setState("fire", 0);
			}
		}


		// check for collisions with the player
		//player_box = player.getHitbox();
		//for (auto& a : asteroids)
		//{
		//	a_box = a.getHitbox();
		//	if (player_box.intersects(a_box))
		//	{
		//		cout << "Hit by asteroid!";
		//		controls.setState("quit", 1);
		//	}
		//}

		// render
		window.clear();
		for (auto& a : asteroids)
			window.draw(a.shape);
		for (auto& s : shots)
			window.draw(s->shape);
		window.draw(player.shape);
		window.display();
	}

	return 0;
}

