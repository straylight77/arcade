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

		int getState(string cmd)			{ return controls[cmd]; }
		void setState(string cmd, int val)	{ controls[cmd] = val; }

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
		bool is_dead = false;

		GameObject() { }

		GameObject(sf::Vector2f p, sf::Vector2f v)
		{
			shape.setPosition(p);
			vel = v;
		}

		GameObject(sf::Vector2f p, float angle, float speed)
		{
			shape.setPosition(p);
			shape.setRotation(angle);
			float x = cos(angle * M_PI / 180.0) * speed;
			float y = sin(angle * M_PI / 180.0) * speed;
			vel = sf::Vector2f(x, y);
		}

		void update()
		{
			shape.move(vel);
			checkBoundary();
		}

		sf::Vector2f getPos()  { return shape.getPosition(); }
		float getAngle()       { return shape.getRotation(); }
		float getSpeed()       { return hypot(vel.x, vel.y); }
		float getDirection()   { return atan2(vel.y, vel.x) * 180.0 / M_PI; }

		sf::FloatRect getHitbox() { return shape.getGlobalBounds(); }

	protected:

		void checkBoundary()
		{
			sf::Vector2f pos = shape.getPosition();
			int width = shape.getGlobalBounds().width / 2;
			int height = shape.getGlobalBounds().height / 2;

			if (pos.x + width < 0)            pos.x = MAX_X + width;     // left side
			else if (pos.x - width > MAX_X)   pos.x = -width;	         // right side

			if (pos.y + height < 0)           pos.y = MAX_Y + height;    // top
			else if (pos.y - height > MAX_Y)  pos.y = -height;           // bottom

			shape.setPosition(pos);
		}
};


//------------------------------------------------------------------------
class Player : public GameObject
{
	public:

		int invincible = false;

		Player(sf::Vector2f p, sf::Vector2f v) :
			GameObject(p, v)
		{
			shape.setPointCount(3);
			shape.setPoint(0, sf::Vector2f(20, 0));
			shape.setPoint(1, sf::Vector2f(-10, 10));
			shape.setPoint(2, sf::Vector2f(-10, -10));
			shape.setFillColor(sf::Color::Black);
			shape.setOutlineColor(sf::Color::White);
			shape.setOutlineThickness(3.0f);
			shape.setOrigin(0, 0);

			reset();
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

			if (invincible > 0)
				invincible--;

			GameObject::update();
		}

		void reset()
		{
			shape.setPosition(sf::Vector2f(MAX_X/2, MAX_Y/2));
			vel = sf::Vector2f(0, 0);
			shape.setRotation(-90);
			invincible = FPS * 3;
			is_dead = false;
		}
};


//------------------------------------------------------------------------
class Asteroid : public GameObject
{
	public:

		int stage;

		Asteroid(int s, sf::Vector2f p, sf::Vector2f v) :
			GameObject(p, v)
		{
			stage = s;
			loadShape(s);
		}

		Asteroid(int s, sf::Vector2f p, float angle, float speed) :
			GameObject(p, angle, speed)
		{
			stage = s;
			loadShape(s);
		}

		Asteroid(int s) :
			Asteroid(s, getRandomPos(), getRandomDirection(), getRandomSpeed(2, 8))
		{ }

	private:

		void loadShape(int stage)
		{
			// Set the number of points based on the stage
			int count;
			switch (stage)
			{
				case 3: count = 9; break;
				case 2: count = 7; break;
				case 1: count = 5; break;
				default: count = 4; break;
			}

			// Set the points for the shape
			shape.setPointCount(count);
			for (int i = 0; i < count; ++i)
			{
				float angle = i * (360.0f / count);
				float radius = stage * 20.0f;
				shape.setPoint(i, sf::Vector2f(
							radius * std::cos(angle * M_PI / 180.0f),
							radius * std::sin(angle * M_PI / 180.0f)
							));
			}

			shape.setFillColor(sf::Color::Black);
			shape.setOutlineThickness(3.0f);
			shape.setOrigin(0, 0);
		}

		static sf::Vector2f getRandomPos()
		{
			// Set a random position within the window bounds
			float posX = static_cast<float>(std::rand() % MAX_X);  // Adjust window width
			float posY = static_cast<float>(std::rand() % MAX_Y);  // Adjust window height
			return sf::Vector2f(posX, posY);
		}

		static sf::Vector2f getRandomVel()
		{
			// Set a random velocity
			float velX = static_cast<float>(std::rand() % 11) - 5; // Random value between -5 and 5
			float velY = static_cast<float>(std::rand() % 11) - 5; // Random value between -5 and 5

			return sf::Vector2f(velX, velY);
		}

		static float getRandomDirection()
		{
			return static_cast<float>(std::rand() % 360);
		}

		static float getRandomSpeed(int low, int high)
		{
			return static_cast<float>((rand() % (high - low + 1)) + low);
		}
};


//------------------------------------------------------------------------
class Shot : public GameObject
{
	public:
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
			time_to_live = FPS;  // FPS * seconds of real-time
		}

		void update()
		{
			//GameObject::update();
			shape.move(vel);
			time_to_live--;
		}


};


//------------------------------------------------------------------------
class Explosion
{
	public:
		int frameCount = 0;
		bool is_dead = false;

		Explosion(sf::Vector2f position, int particleCount, float speed, int frames)
			: position(position), speed(speed)
		{
			for (int i = 0; i < particleCount; ++i)
			{
				frameCount = frames;
				sf::CircleShape particle(2.0f);
				particle.setPosition(position);
				//particle.setFillColor(sf::Color::Yellow);

				float angle = (2 * M_PI / particleCount) * i;
				float x = std::cos(angle) * speed;
				float y = std::sin(angle) * speed;

				particle.move(x, y);

				particles.push_back(particle);
			}
		}

		void update()
		{
			if (frameCount <= 0) {
				is_dead = true;
				return;
			}

			for (auto& particle : particles)
			{
				float angle = std::atan2(
						particle.getPosition().y - position.y,
						particle.getPosition().x - position.x);
				float x = std::cos(angle) * speed;
				float y = std::sin(angle) * speed;

				particle.move(x, y);
			}

			frameCount--;
		}

		void draw(sf::RenderWindow& window)
		{
			for (const auto& particle : particles)
				window.draw(particle);
		}

	private:
		sf::Vector2f position;
		float speed;
		std::vector<sf::CircleShape> particles;
};


//------------------------------------------------------------------------
class Game
{
	public:

		//----------------------------------------------------------------
		Game():
			window(sf::VideoMode(MAX_X, MAX_Y), "Classic Asteroids"),
			player(sf::Vector2f(MAX_X/2, MAX_Y/2), sf::Vector2f(0, 0))
		{
			window.setFramerateLimit(FPS);
			srand(static_cast<unsigned>(time(nullptr)));
			font.loadFromFile("/usr/share/fonts/chromeos/monotype/verdana.ttf");
			info_text.setFont(font);
			info_text.setCharacterSize(32);
			info_text.setFillColor(sf::Color(192, 192, 192));

			create_level();
		}

		//----------------------------------------------------------------
		void start()
		{
			while (window.isOpen() && !controls.getState("quit"))
			{

				//TODO:
				//	add delay_frames - # of frames to ignore input, update
				//  game_state - playing, game over, new level, title screen
				//  invincible - # of frames that player cannot die, ship flashes

				handle_input();
				update();
				asteroid_shot_collisions();
				asteroid_player_collisions();
				remove_dead_objects();

				if (player.is_dead && explosions.size() == 0)
				{
					lives--;
					if (lives > 0)
						player.reset();
					else
					{
						cout << "Game Over!\n";
						cout << "Final score: " << to_string(score) << "\n";
						controls.setState("quit", 1);
					}
				}

				if (asteroids.size() <= 0 && explosions.size() == 0)
				{
					level++;
					create_level();
					player.reset();
				}

				render();
			}
		}

	private:

		sf::RenderWindow window;
		GameControls controls;
		sf::Font font;
		sf::Text info_text;

		int score = 0;
		int lives = 3;
		int level = 1;

		Player player;
		vector<std::shared_ptr<Shot>> shots;
		vector<std::shared_ptr<Asteroid>> asteroids;
		vector<std::shared_ptr<Explosion>> explosions;

		//----------------------------------------------------------------
		void handle_input()
		{
			sf::Event event;
			while (window.pollEvent(event))
			{
				controls.handleEvent(event);
				if (controls.getState("quit"))
					window.close();
			}
		}

		//----------------------------------------------------------------
		void update()
		{
			for (auto& a : asteroids)
				a->update();

			for (auto& e : explosions)
				e->update();

			for (auto s = shots.begin(); s != shots.end(); /* no increment */)
			{
				(*s)->update();

				if ((*s)->time_to_live <= 0)
					s = shots.erase(s);
				else
					++s;
			}

			if (!player.is_dead)
			{
				player.update(controls);

				if (controls.getState("fire"))
				{
					if (shots.size() < 3) // limit number of active shots
					{
						shots.push_back(std::make_shared<Shot>( player.getPos(), player.getAngle() ));
						controls.setState("fire", 0);
					}
				}
			}

			info_text.setString(
				"LEVEL: " + to_string(level)
				+ "     SHIPS: " + to_string(lives)
				+ "     SCORE: " + to_string(score)
				//+ "     Asteroids: " + to_string((int)asteroids.size())
				//+ "     Explosions: " + to_string((int)explosions.size())
			);
		}

		//----------------------------------------------------------------
		void asteroid_shot_collisions()
		{
			std::vector<std::shared_ptr<Asteroid>> new_asteroids;
			for (const auto& obj1 : asteroids)
			{
				for (const auto& obj2 : shots)
				{
					if (obj1->getHitbox().intersects(obj2->getHitbox()))
					{
						if (asteroids.size() > 1)
							explosions.push_back(std::make_shared<Explosion>(obj1->getPos(), 10, 3.0f, 15));
						else
							explosions.push_back(std::make_shared<Explosion>(obj1->getPos(), 10, 3.0f, 45));

						// increase score
						score += 10;
						// create new asteroids
						if (obj1->stage > 1)
						{
							int new_stage = obj1->stage - 1;
							sf::Vector2f new_pos = obj1->getPos();
							float new_speed = obj1->getSpeed();
							float new_angle = obj1->getDirection();
							new_asteroids.push_back(std::make_shared<Asteroid>(new_stage, new_pos, new_angle-55.0, new_speed));
							new_asteroids.push_back(std::make_shared<Asteroid>(new_stage, new_pos, new_angle+55.0, new_speed));
						}
						// mark a and s for deletion
						obj1->is_dead = true;
						obj2->is_dead = true;
					}
				}
			}
			asteroids.insert(asteroids.end(), new_asteroids.begin(), new_asteroids.end());
		}

		//----------------------------------------------------------------
		void asteroid_player_collisions()
		{
			if (player.is_dead || player.invincible)
				return;

			for (const auto& obj1 : asteroids)
			{
				if (obj1->getHitbox().intersects(player.getHitbox()))
				{
					player.is_dead = true;
					explosions.push_back(std::make_shared<Explosion>(player.getPos(), 30, 4.0f, 60));
				}
			}
		}


		//----------------------------------------------------------------
		void render()
		{
			window.clear();
			for (auto& a : asteroids)   window.draw(a->shape);
			for (auto& e : explosions)  e->draw(window);
			for (auto& s : shots)       window.draw(s->shape);
			if (!player.is_dead && player.invincible % 16 < 8)
				window.draw(player.shape);
			window.draw(info_text);
			window.display();
		}

		//----------------------------------------------------------------
		void create_level()
		{
			int num = level % 3;
			for (int i = 0; i < num; i++)
			{
				asteroids.push_back(std::make_shared<Asteroid>(3));
			}
		}

		//----------------------------------------------------------------
		void remove_dead_objects()
		{
			asteroids.erase(
					std::remove_if(
						asteroids.begin(),
						asteroids.end(),
						[](const auto& obj) { return obj->is_dead; }),
					asteroids.end());

			shots.erase(
					std::remove_if(
						shots.begin(),
						shots.end(),
						[](const auto& obj) { return obj->is_dead; }),
					shots.end());

			explosions.erase(
					std::remove_if(
						explosions.begin(),
						explosions.end(),
						[](const auto& obj) { return obj->is_dead; }),
					explosions.end());

		}

};


/*************************************************************************/
int main()
{
	Game g;
	g.start();
	return 0;
}

