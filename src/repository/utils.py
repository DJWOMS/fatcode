def repository_stats(project, repository):
    project.star_count = repository.stargazers_count
    project.fork_count = repository.forks_count

    project_commits = repository.get_commits()
    project.commit_count = project_commits.totalCount

    last_commit = repository.get_commit(project_commits[0].sha)
    project.last_commit = last_commit.commit.committer.date

    project.save()
