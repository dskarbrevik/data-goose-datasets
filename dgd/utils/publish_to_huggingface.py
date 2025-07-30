"""
Module to publish a dataset to Hugging Face Hub using the huggingface_hub library.
"""

from pathlib import Path
from huggingface_hub import HfApi, HfFolder, Repository

def publish_dataset_to_huggingface(
    dataset_path: str,
    repo_id: str,
    token: str = None,
    repo_type: str = "dataset",
    commit_message: str = "Add dataset"
) -> str:
    """
    Publishes a dataset to the Hugging Face Hub.

    Args:
        dataset_path (str): Local path to the dataset directory or file.
        repo_id (str): The repo id in the format 'username/dataset_name'.
        token (str, optional): Hugging Face access token. If None, will use the token from cache.
        repo_type (str, optional): Type of repo, default is 'dataset'.
        commit_message (str, optional): Commit message for the upload.

    Returns:
        str: The URL of the published dataset on Hugging Face Hub.
    """

    if token is None:
        token = HfFolder.get_token()
        if token is None:
            raise ValueError("No Hugging Face token found. Please login using 'huggingface-cli login'.")

    api = HfApi()
    # Create repo if it doesn't exist
    api.create_repo(repo_id=repo_id, token=token, repo_type=repo_type, exist_ok=True)

    # Clone repo locally (in a temp dir)
    from tempfile import TemporaryDirectory
    import shutil
    dataset_path = Path(dataset_path)
    with TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        repo = Repository(local_dir=tmpdir, clone_from=repo_id, repo_type=repo_type, token=token)
        repo.git_pull()

        # Copy dataset files into repo using pathlib
        if dataset_path.is_dir():
            for item in dataset_path.iterdir():
                dest = tmpdir_path / item.name
                if item.is_dir():
                    shutil.copytree(item, dest, dirs_exist_ok=True)
                else:
                    shutil.copy2(item, dest)
        else:
            shutil.copy2(dataset_path, tmpdir_path)

        repo.git_add()
        repo.git_commit(commit_message)
        repo.git_push()

    url = f"https://huggingface.co/datasets/{repo_id}"
    return url
