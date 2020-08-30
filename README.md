perx_testcase
=================

Perx company test assignment


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

	6. Start api backend:
	$ docker-compose up api

	Browse http://localhost:8000 to see django hello page (DEBUG=True)

	7. Run client sample:
	$ cd exsample
	$ python3 client.py

	$ docker-compose up adminer
	browse http://localhost:8081/


Details
=================

	* Максимальный размер файла установлен 80М. nginx может и больше, но даже с таким размеров все же лучше усложнять API и делать загрузку по частям.
	  Если клиенты свои, а документы известного формата, можно и обойтись.
	*

