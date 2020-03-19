# Robs quick guide to git 

## starting a new project, local repo and remote
1. to start a new repo open the git bash program
2. go to the folder that you want to be the root of the repo    
    use cd /c/users/etc for the navigation, linux stylee
3. once there use git init to initialize init
4. now make your .gitignore file, uses standard *.* etc notation, and for folders dont use the first / but put on at the end
5. now do 
    git add .
    this will add the files in the folder which arent being ignored to the prep for the repo
6. now need to commit:
    git commit
        now there are two options, 
            one is to hit enter, it will open up the git commit in the editor, you need to add the commit message there
            second is to use '-m "message content here' after the git commit, does the same thing from the commant line
7. now we need to connect to the github repo, see here:
    https://help.github.com/en/articles/adding-a-remote
    aka:
        a. git remote add origin https://whatever.github.url
        b. git remote -v
8. now push local to the remote repo    
    git push origin master
        or
    git push https://whatever.github.url master

## update files locally and remotely:

1. do the add, either for precise file or all
    git add .       (all the files)
    git add file_name.end
2. then commit
    git commit
3. then push to the remote
    git push origin master

## pull files from github repo:

1. git pull origin master

## Remove files or directory from repo

1. see here: https://stackoverflow.com/questions/1143796/remove-a-file-from-a-git-repository-without-deleting-it-from-the-local-filesyste
2. for a file
    git rm --cached mylogfile.log
3. for a single directory:
    git rm --cached -r mydirectory

## Forking a git repo

## Others

1. Change folder in git bash:
    https://stackoverflow.com/questions/8961334/how-to-change-folder-with-git-bash
2. List files in repo:
    git ls-files 
3. Test 