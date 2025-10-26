# Contributing to nltk_data

Thank you for your interest in contributing to [`nltk_data`](https://github.com/nltk/nltk_data)! This guide will help you add new data packages (corpora, taggers, models, etc.) and contribute improvements to existing ones.

## Adding a New Data Package

The `nltk_data` repository contains datasets and resources that can be downloaded by `nltk.downloader`. To add a new dataset or resource, please follow these steps:

### 1. Fork and Clone the Repository

First, fork the [`nltk_data`](https://github.com/nltk/nltk_data) repository to your own GitHub account. For help with forking, see the [GitHub documentation on forking a repository](https://docs.github.com/en/get-started/quickstart/fork-a-repo).

Then, clone your fork locally:

```bash
git clone https://github.com/<your-github-username>/nltk_data.git
cd nltk_data
```

### 2. Create a New Branch

Create a branch for your dataset:

```bash
git checkout -b add-my-dataset
```

### 3. Add Your Data Package

- Place your dataset in the appropriate directory (`corpora/`, `models/`, `tokenizers/`, etc.). If you are unsure, check the existing structure or open an issue for clarification.
- If your dataset has a license, include the license file in the same directory. If the license is unknown or separate from the repository, please add a note in a `README` or `LICENSE` file within the dataset’s folder, and document this in your pull request.

**Whenever you add a new data package, you must update [`DATASET-LICENSES.md`](DATASET-LICENSES.md) with the license information for your package.**

You only need to update [`LICENSE-OVERVIEW.md`](LICENSE-OVERVIEW.md) if you are making changes to the repository’s overall licensing structure or guidance.

### 4. Update Index Files

- You do **not** need to manually update `index.xml`. This file is now rebuilt automatically by a GitHub Actions workflow after your changes are merged.
- Any local changes you make to `index.xml` will be ignored and overwritten by the workflow.
- Provide a short README or metadata file describing the package, its origin, and its license.

### 5. Commit and Push Your Changes

```bash
git add <your new files>
git commit -m "Add <name> dataset to nltk_data"
git push origin add-my-dataset
```

### 6. Create a Pull Request

Open a pull request from your branch to the `master` branch of `nltk/nltk_data`. For help, see the [GitHub documentation on creating a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request).

In your pull request, please include:
- A description of the dataset and its purpose.
- Any relevant licensing information or restrictions.
- Instructions for any special installation or usage requirements.

### 7. Respond to Feedback

- Be responsive to comments and requested changes.
- If your dataset cannot be accepted (e.g., due to licensing issues), we will let you know in the pull request.

## General Guidelines

- **Licensing**: Please ensure you have the right to redistribute any data you submit, and document the license clearly. If the license is unknown, state this explicitly in your pull request.
- **No Large Files**: If your package is extremely large, consider hosting it elsewhere and providing an index/manifest, or open an issue to discuss options.
- **No Executable Files**: Only data, not code, should be included unless a script is essential for using the dataset.

## Additional Resources

- [GitHub Docs: Fork a repo](https://docs.github.com/en/get-started/quickstart/fork-a-repo)
- [GitHub Docs: Branches](https://docs.github.com/en/get-started/quickstart/github-glossary#branch)
- [GitHub Docs: Pull Requests](https://docs.github.com/en/pull-requests)

If you have questions or need help, please open an issue or join the [nltk-dev mailing list](https://groups.google.com/forum/#!forum/nltk-dev).

---

Thank you for helping improve NLTK’s data resources!