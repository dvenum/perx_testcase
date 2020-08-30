perx_testcase
=================

Perx company test assignment
https://gist.github.com/abj/a073ca103839b20e9876bf09c9791656


Installation
=================

	1. Get source code:
	$ git clone https://github.com/dvenum/perx_testcase.git
	$ cd perx_testcase

	2. Set keys and passwords. Generate your own keys:
	Fill .env_sample and save it as '.env'.
	Fill core/secrets.py_ and save it as 'core/secrets.py'.

	3. Build base docker image:
	$ docker-compose build

	4. Apply migrations:
	$ docker-compose up migration

	5. Run tests:
	$ docker-compose up test

	6. Run ./manage.py collectstatic for /admin/, if you like

	7. Start api backend:
	$ docker-compose up api

	Browse http://localhost:8000 to see django hello page (DEBUG=True)

	8. Visit http://localhost:8000/admin/
	   Create new Token for admin or make your own user.
	   Copy token (ex.: '40e787c88ecf0c5e7c01de8b2adfbc978432fb9b') to example/.token

	9. Run client sample:
	$ cd example
	$ python3 client.py

	10. Runt tests:
	$ docker-compose up test


	Misc:
	$ docker-compose up adminer
	browse http://localhost:8081/


Details
=================

	* Максимальный размер файла установлен 80М. nginx может и больше, но даже с таким размеров все же лучше усложнять API и делать загрузку по частям.
	  Если клиенты свои, а документы известного формата, можно и обойтись.

