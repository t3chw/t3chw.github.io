---
layout: post
title: "Step-by-Step Guide to Creating a Personal Blog with GitHub Pages and Jekyll"
date: 2025-01-18 12:00:00 +0000
categories: [Tech]
tags: [GitHub, Jekyll, Blogging]
---

Welcome to my personal blog! This post is a detailed step-by-step guide to creating your own personal blog using **GitHub Pages** and **Jekyll**. Follow these steps carefully, and you'll have your blog up and running in no time.

---

## Steps to Create Your Blog

### **1. Fork the Jekyll Theme**
- Visit the [https://github.com/cotes2020/chirpy-starter] repository.
- Click **"Use this template"** to create a new repository in your GitHub account.
- Name the repository `<your-username>.github.io` (replace `<your-username>` with your GitHub username).
- Click **Create repository**.

---

### **2. Configure Your Repository**
- Open the `_config.yml` file in the repository.
- Edit the following:
  - **URL:**
    ```yaml
    url: "https://<your-username>.github.io"
    ```
  - **Title and Description:**
    ```yaml
    title: "My Personal Blog"
    description: "A blog about coding, tech, and life."
    ```
- Commit your changes with a meaningful message like "Updated blog configuration".

---

### **3. Enable GitHub Pages**
- Navigate to the **Settings** tab of your repository.
- Under **Pages**, select the `main` branch as the source.
- Save the settings. Your blog will be live at:
  ```
  https://<your-username>.github.io
  ```

---

### **4. Clone the Repository Locally**
- Open a terminal or command prompt.
- Run the following commands:
  ```bash
  git clone https://github.com/<your-username>/<your-username>.github.io.git
  cd <your-username>.github.io
  ```

---

### **5. Set Up Your Development Environment**
- Install **Ruby** and **Bundler**:
  - Ruby & Jekyll Installation: https://jekyllrb.com/docs/installation/
  - Install Bundler:
    ```bash
    gem install bundler
    ```
- Install project dependencies:
  ```bash
  bundle 
  ```

---

### **6. Run Your Blog Locally**
- To preview your blog locally, start the Jekyll server:
  ```bash
  bundle exec jekyll serve
  ```
- Open your browser and visit:
  ```
  http://127.0.0.1:4000
  ```

---

### **7. Customize Your Blog**
- Open the `_config.yml` file to make customizations:
  - Update the `title`, `description`, and `social links`.
  - Add an avatar image:
    ```yaml
    avatar: "<link-to-your-image>"
    ```

---

### **8. Write Your First Blog Post**
- Navigate to the `_posts` folder in your project directory.
- Create a new markdown file with this format:
  ```
  YYYY-MM-DD-title.md
  ```
- Add the following content:
  ```markdown
  ---
  layout: post
  title: "My First Blog Post"
  date: YYYY-MM-DD HH:MM:SS +0000
  categories: [Example]
  tags: [Getting Started]
  ---
  Welcome to my blog! This is my first post.
  ```
- Save the file.

---

### **9. Push Changes to GitHub**
- Stage and commit your changes:
  ```bash
  git add .
  git commit -m "Added first blog post and customizations"
  ```
- Push your changes:
  ```bash
  git push origin main
  ```

---

### **10. Enable LiveReload for Automatic Browser Updates**
- Install the `jekyll-livereload` gem:
  ```bash
  gem install jekyll-livereload
  ```
- Add it to your `Gemfile`:
  ```ruby
  group :jekyll_plugins do
    gem 'jekyll-livereload'
  end
  ```
- Install the gem via Bundler:
  ```bash
  bundle install
  ```
- Run the server with LiveReload:
  ```bash
  bundle exec jekyll serve --livereload
  ```

---

### **11. Optional: Use a Custom Domain**
- Purchase a domain (e.g., from GoDaddy or Namecheap).
- Update the DNS settings:
  - Add `A` records pointing to:
    ```
    185.199.108.153
    185.199.109.153
    185.199.110.153
    185.199.111.153
    ```
  - Add a `CNAME` record pointing to:
    ```
    <your-username>.github.io
    ```
- In GitHub repository settings, under **Pages**, add the custom domain.

---

## Final Thoughts

Creating a personal blog using GitHub Pages and Jekyll is simple, cost-effective, and highly customizable. Follow these steps, and you’ll have a professional-looking blog in no time.

