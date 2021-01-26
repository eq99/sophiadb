import os
from datetime import datetime
from flask import jsonify, Blueprint
from flask_restful import Resource, reqparse
from werkzeug.exceptions import NotFound
from plugins import api
from utils.timezones import FixedOffset

from pygit2 import (
  Repository, 
  init_repository,
  GIT_OBJ_COMMIT, 
  GIT_OBJ_BLOB, 
  GIT_OBJ_TREE, 
  GIT_OBJ_TAG, 
  GIT_REF_SYMBOLIC)

repo_bp = Blueprint('repo', __name__,url_prefix='/api')

BASE_DIR = 'D:\\tmp\\'
def detect_repos(path, depth=5):
    for dirent in os.scandir(path):
        if not dirent.is_dir():
            continue
        if dirent.name == '.git':
            yield path
            break
        if dirent.name.endswith('.git'):
            yield dirent.path
            continue
        if depth > 1:
            yield from detect_repos(dirent.path, depth=depth-1)

def get_repo_names():
  prefix = BASE_DIR
  prefix_len = len(prefix)
  relative_repo_paths = (path[prefix_len:] for path in detect_repos(prefix)
                          if path.startswith(prefix))
  return {rel_path for rel_path in relative_repo_paths}

def get_repo(repo_name):
  repo_path = f'{BASE_DIR}{repo_name}/.git'
  return Repository(repo_path)



def parse_signature(sig):
  return {
    "name": sig.name,
    "email": sig.email,
    "date": datetime.fromtimestamp(sig.time, FixedOffset(sig.offset))
  }

class RepoAPI(Resource):
  def __init__(self):
    self.parser = reqparse.RequestParser(bundle_errors=True)
    self.parser.add_argument('repo_name', required=True, help='repo name is required')

  def get(self):
    data = list(get_repo_names())
    return jsonify(
      message='return repos',
      data=data,
      status=200
    )

  def post(self, repo_name):
    repo = init_repository(f'{BASE_DIR}{repo_name}/')
    return jsonify(
      massage='init repo successful',
      data=str(repo),
      status=201
    )

api.add_resource(RepoAPI, '/repo', '/repo/<repo_name>')


def get_commit_for_refspec(repo, branch_or_tag_or_sha):
    try:
        commit = repo.revparse_single(branch_or_tag_or_sha)
        if commit.type == GIT_OBJ_TAG:
            commit = commit.peel(GIT_OBJ_COMMIT)
        return commit
    except KeyError:
        raise NotFound("no such branch, tag, or commit SHA")


class CommitAPI(Resource):

  def __init__(self):
    self.parser = reqparse.RequestParser(bundle_errors=True)
    self.parser.add_argument('file_name', required=True, help='file_name required')
    self.parser.add_argument('file_content', required=True, help='file_content required')
  
  def get(self, repo_name):
    '''Get commit of master
    uri: /api/repo/<repo_name>/master
    '''
    repo = get_repo(repo_name)
    commit = get_commit_for_refspec(repo, 'master')

    data = {
      'sha': str(commit.id),
      'author': parse_signature(commit.author),
      'committer': parse_signature(commit.committer),
      'message': commit.message.rstrip(),
      'tree': {
        'sha': str(commit.tree_id),
      },
      'parents': [{
        'sha': str(c.id),
      } for c in commit.parents]
    }

    return jsonify(
      data=data,
      status=200
      )

api.add_resource(CommitAPI, '/repo/<repo_name>/master')

class FilesAPI(Resource):
  def get(self, repo_name):
    '''Get lastest tree of master
    uri: /api/repo/<repo_name>/master/tree
    '''
    repo = get_repo(repo_name)
    commit = get_commit_for_refspec(repo, 'master')
    tree_id = commit.tree_id,


  def post(self):
    '''Create a new file.
    uri: /api/repo/<repo_name>/files
    '''
    args = self.parser.parse_args()
    file_name = args.file_name
    file_content = args.file_content

    return jsonify(
      message='create file {file_name}',
      data='',
      status=201
    )

api.add_resource(FilesAPI, '/repo/<repo_name>/files')


class FileAPI(Resource):

  def get(self):
    '''Get data about a file
    '''
    pass

  def put(self):
    '''Modify a file
    '''
    pass
