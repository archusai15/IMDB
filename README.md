1. Data model used to design the table structures is shown in Data Model.pptx
2. Overall process used to build the project is shown in Process.pptx
3. Transform_Data.py script is used to clean and transform data according to data model. Upon executing, it will generate all the input files (in CSV format)
4. Insert_Data.py script is used to establish database connection, create tables and insert data. Before executing this file, docker container must be started. SQL container in docker was used for this project - steps to install docker and instantiate SQL is given in docker_install_steps.docx
5. config.json file has all the variables used in the python script. It must be placed in the same folder as python scripts to execute both the scripts. Local file path and database credentials must be updated with yours in order to run successfully
6. Input files are also uploaded to get a better view of the structure
7. Future Work - More fact tables including 2/3 dimensions and aggregations/ calculations can be added for analytical purpose
