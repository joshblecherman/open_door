# Set Up 

## Step 1: create a virtualenv 

We want a virtual environment that has our python version and all dependencies installed locally within a contained environment

<a href="https://docs.python.org/3/library/venv.html">Python's guide to venv</a>
<ol> 
    <li>Download python 3.11 (That's what I am using, and we should all use the same version)</li>
    <li>Make sure that when you run:<pre>python3 --version</pre>
    you see:
    <pre>Python 3.11.0</pre></li>
    <li>Create a directory where you want to store your virtual env. I have a venvs folder on my desktop.</li>
    <li>Run this:<pre>python3 -m venv /path/to/venvs/folder/open_door</pre></li>
    This will create a virtualenv called open_door in the directory you made in step 3.
</ol>

## Step 2: create project 

Create a project attach the virtualenv we just made as the interpreter. I am using PyCharm - steps will vary if you are using VSCode.

<ol>
    <li>Open PyCharm. Click “new project”</li>
    <li>Add interpreter > Add local interpreter</li> 
    <li>Click “existing”</li>
    <li>Change interpreter path to <pre>path/to/virtualenv/bin/python3.11</pre>
</li>
    <li>Click create</li>
</ol>

## Step 3: install git (skip if you have it already)

For mac:
<ol>
    <li>install brew</li> 
    <li>run: <pre>brew install git</pre></li>
</ol>

## Step 4: setup git 
<ol>
    <li>Navigate to the project you created in step 3</li>
    <li>Not technically necessary for git, but whenever you are working on the project you should activate the virtual environment. Run: <pre>source /path/to/virtualenv/bin/activate</pre>
    Whenever you want to exit the virtualenv run: 
    <pre>deactivate</pre>
    </li>
    <li>run <pre>git init</pre> You should see something like the following: 
    <pre>Initialized empty Git repository in /Users/joshblecherman/Desktop/projects/open_door/.git/</pre></li> 
    <li>I'll add more instructions later...</li>
</ol>


# Links to Read

* Quickstart for flask: https://flask.palletsprojects.com/en/2.2.x/quickstart/  
* Simple flask tutorial: https://flask.palletsprojects.com/en/2.2.x/tutorial/ 

