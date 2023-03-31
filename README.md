# Intro

# 爬虫

主入口为：https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search

- Linkedin 开放的 API
- 无需登录
- 数据获取上有一定的限制
    - 无法直接获取到岗位相关 skills 和大部分的 salary 数据

JD 入口在 `<section class="two-pane-serp-page__results-list">` 内的 `<a class="base-card__full-link">` 链接