# Repository for Submitting Labs in STAT 214, Spring 2025

## Setup

Your report and code will be submitted via GitHub. The following instructions will show you how to set up your GitHub account and configure a repository so that you can submit your assignments. This workflow is shamelessly copied (with moderate modifications) from Chris Paciorek and Jarod Millman's STAT243 class in 2014.

1. If you are not on a Unix system (e.g. Linux or MacOS or WSL), get on one. Ask me how or refer to the instructions previously given by the GSI.

1. Install Git on your system if it is not there already (https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

1. Sign up for GitHub (https://github.com/).

1. Highly recommended: Go to https://education.github.com/students and sign up for the student pack. This will give you free access to GitHub Copilot. Do this sooner rather than later as the verification process can take a week.

Once you have completed these first steps, you are then ready to create your private GitHub repository for this class. All of the following instructions should be done only on the GitHub website and in the command line. **Do not** use the GitHub Desktop app or any other GUI, as they may do things another way which messes things up.

1. On the GitHub website, log in and create a **private** remote repository called `stat-214`. That must be its exact name! **Do not** check the boxes to "Add .gitignore" or "Choose a license" (we will provide .gitignore). After you hit "Create repository", you will be able to see it at https://github.com/YOURUSERNAME/stat-214. Note that your repository will be empty.

1. Add the GSIs (`zachrewolinski`, `austinvzane`, and `aagarwal1996`) as collaborators on your private repository so that we can access it (on https://github.com/YOURUSERNAME/stat-214, navigate to Settings -> Collaborators -> Add people).

1. Open your terminal and navigate to the directory where you keep your 214 work. For example, I would do `cd grad/214` to enter my `214` directory in my `grad` folder.

1. Using the command-line, clone your stat-214 repository: `git clone https://github.com/YOURUSERNAME/stat-214`. This will create a copy of your `stat-214` repository on your own computer.

1. If you are prompted for a username, enter your GitHub username. If you are prompted for a password, you must enter a GitHub access token (If you use your GitHub password, you will see an authentication error). If you don't have one yet, you can make an access token at https://github.com/settings/tokens/new. Feel free to set the expiration to "No expiration" (though that is not super secure...). The only box you need to check under "Select scopes" is "repo". After you create the token, make sure to copy it and save it somewhere, as you will never see it again.

1. Move the `.gitignore` and `info.txt` files from `stat-214-gsi` into the base directory of your `stat-214` repository (aka, not in an inner folder). You should have already cloned the `stat-214-gsi` repository - see the last slide of the first discussion for details.

1. Now, edit *info.txt* in your local `stat-214` repository to reflect your own information.

```
name = "Jane Smith"
SID = "0123456789"
email = "jsmith@berkeley.edu"
github_name = "janesmith"
```

1. In your terminal while you are in the `stat-214` repository directory, check git status `git status`. You should see a bunch of text including `modified:   info.txt`.

1. Add the files (`git add info.txt .gitignore`) and commit (`git commit -m “Updated info.txt with my own information and added .gitignore”`).

1. Push your changes to your copy of the remote repository (`git push` or sometimes `git push remote origin`)

1. Check that info.txt has been updated in your remote github repository by navigating to https://github.com/YOURUSERNAME/stat-214 (change YOURUSERNAME to your username).

## Submitting your projects

To submit your projects, you will need to create a subfolder in your local `stat-214` folder called `lab1` (if you are submitting lab 1). The precise structure of the `lab1` folder is described in the `lab-instructions.pdf` file in the `stat-214-gsi` repo.

Note that GitHub cannot host files more than 100 MB. If you try to push a file larger than this, GitHub will cry. This means you should avoid pushing the data to your GitHub.  

When you are ready, you need to add, commit, and push the `lab1/` folder.

At the time when the lab is due, we will run a script that automatically pulls all of your assignments into my local versions of your `stat-214` repositories. Please make sure to submit your labs on time. `lab0` is a pretend assignment which you will complete to make sure that you are all clear on what to do.

Note: this document was originally written by Rebecca Barter in Fall 2017 and edited by successive GSIs to reflect the changes in the course.  
