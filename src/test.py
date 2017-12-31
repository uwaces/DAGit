import git

git = repo.git
    
git.checkout('HEAD', b="my_new_branch")         # create a new branch
git.branch('another-new-one')
git.branch('-D', 'another-new-one')             # pass strings for full control over argument order
git.for_each_ref()                              # '-' becomes '_' when calling it