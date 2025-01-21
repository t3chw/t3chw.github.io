---
layout: post
title: "Mastering GitHub, Poetry, Ruff, and Black: A Step-by-Step Guide"
date: 2025-01-16 12:00:00 +0000
categories: [Tech]
tags: [GitHub, Poetry, Ruff]
---

When managing a project with tools like GitHub, Poetry, Ruff, and Black, having a streamlined workflow is essential. This guide will help you navigate the commands and best practices for version control, dependency management, and code formatting.

---

## **Step-by-Step Workflow**

### **1. Cloning the Repository**
Start by cloning the repository to your local machine:
```bash
git clone https://<username>@bitbucket.org/<repository-owner>/<repository-name>.git
cd <repository-name>
```

---

### **2. Installing Dependencies with Poetry**
If your project uses Poetry for dependency management, install all required dependencies:
```bash
poetry install --sync
```

This ensures all dependencies listed in `pyproject.toml` and `poetry.lock` are installed.

---

### **3. Activating the Poetry Environment**
Activate the Poetry virtual environment to ensure all subsequent commands (e.g., linting, testing) run within the correct environment:
```bash
poetry shell
```

---

### **4. Checking the Status**
View the current status of your working directory to see any unstaged changes or untracked files:
```bash
git status
```

---

### **5. Create a New Branch**

Start by creating a new branch for your feature or bug fix. Use the following command:

```bash
git checkout -b feature/<branch-name>
```

#### Example:
```bash
git checkout -b feature/univariate-time-series
```

This creates and switches to the new branch `feature/univariate-time-series`.

---

### **6. Work on Your Changes**

Make your edits to the code. Periodically, check the status of your working directory to see what has been modified:

```bash
git status
```

---

### **7. Linting and Formatting**
Before staging or committing your changes, ensure your code adheres to formatting and linting standards:

#### **7.1 Using Ruff for Linting**
- Check for issues:
  ```bash
  ruff check .
  ```
- Fix issues automatically:
  ```bash
  ruff check . --fix
  ```

#### **7.2 Using Black for Formatting**
- Check formatting:
  ```bash
  black . --check
  ```
- Apply formatting:
  ```bash
  black . --line-length 120
  ```

---

### **8. Testing the Code**
Run your tests to ensure your changes don’t break existing functionality:

- Run all tests:
  ```bash
  pytest
  ```

- Run specific tests:
  ```bash
  pytest path/to/test_file.py::test_function_name
  ```

---

### **9. Stage Your Changes**

Once your code passes linting, formatting, and testing, stage the files you want to commit:

#### To stage specific files:
```bash
git add <file-path>
```

#### To stage all changes:
```bash
git add .
```

---

### **10. Commit Your Changes**

Create a commit with a clear, descriptive message:

```bash
git commit -m "Add feature for univariate time series analysis"
```

---

### **11. Push the Branch**

Push your branch to the remote repository so it can be shared with others:

```bash
git push origin feature/<branch-name>
```

#### Example:
```bash
git push origin feature/univariate-time-series
```

---

### **12. Open a Pull Request (PR)**

After pushing your branch, open a **Pull Request (PR)** or **Merge Request (MR)** on your Git hosting platform (e.g., GitHub, Bitbucket, GitLab). This allows your team to:

1. Review your changes.
2. Run tests or CI/CD pipelines.
3. Provide feedback before merging into the main branch.

---

## **Why Not Commit Directly to `main` or `master`?**

Directly committing to the `main` branch can lead to several issues:

1. **Breaking the Production Code**:
   - Incomplete or buggy changes might break the stable branch.

2. **Harder Rollbacks**:
   - If something goes wrong, undoing changes on the `main` branch can be messy and disruptive.

3. **Poor Collaboration**:
   - Direct commits don’t give other team members a chance to review or provide feedback.

Using branches ensures better organization, collaboration, and stability.

---

## **Key Commands Summary**

### **Branching**
- Clone the repository:
  ```bash
  git clone https://<username>@bitbucket.org/<repository-owner>/<repository-name>.git
  ```
- Install dependencies:
  ```bash
  poetry install
  ```
- Activate the Poetry environment:
  ```bash
  poetry shell
  ```
- Create and switch to a new branch:
  ```bash
  git checkout -b feature/<branch-name>
  ```

### **Staging and Committing**
- Stage changes:
  ```bash
  git add .
  ```
- Commit changes:
  ```bash
  git commit -m "Your commit message"
  ```

### **Pushing Changes**
- Push the branch to remote:
  ```bash
  git push origin feature/<branch-name>
  ```

---

## **Using Pre-Commit Hooks**

Pre-commit hooks automate checks like linting and formatting before every commit.

- **Install Pre-Commit Hooks**:
  ```bash
  pre-commit install
  ```

- **Run Hooks Manually**:
  ```bash
  pre-commit run --all-files
  ```

- **Bypass Hooks (if necessary)**:
  ```bash
  git commit -m "Your commit message" --no-verify
  ```

---

## **Debugging Common Issues**

### **1. Dependency Mismatch**

If `poetry.lock` is outdated:
1. Regenerate the lock file:
   ```bash
   poetry lock
   ```

2. Reinstall dependencies:
   ```bash
   poetry install
   ```

---

### **2. Authentication Issues**

For private repositories (e.g., AWS CodeArtifact):

```bash
export POETRY_HTTP_BASIC_ARTIFACT_USERNAME=aws
export POETRY_HTTP_BASIC_ARTIFACT_PASSWORD=<your-token>
```

---

## **Best Practices**

1. Always lint, format, and test your code before committing.
2. Use clear and descriptive commit messages.
3. Create a new branch for each feature, bug fix, or experiment.
4. Push changes frequently to back up your work.
5. Use Pull Requests (PRs) for code review and feedback.
6. Avoid committing directly to the `main` branch.

---

By following this workflow, you’ll ensure your development process is collaborative, organized, and safe for production.
