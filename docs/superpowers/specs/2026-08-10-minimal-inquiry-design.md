# ChemNorm 极简询盘设计

## 目标

降低首次询盘门槛，让客户只需确认产品、填写邮箱并发送预置需求。

## 页面结构

- 顶部产品摘要：分子结构图、产品名、CAS、Product ID。
- 必填：工作邮箱、需求描述。
- 选填：姓名、公司或机构。
- 默认需求：`Please quote this product and provide availability, purity, package options and lead time.`
- 提示：通常在一个工作日内回复。

## 提交流程

提交至现有 Formspree 表单；成功后进入站内成功页，并显示产品摘要、客户需求及关联产品。失败时留在当前页面并显示明确错误。

## 发布检查

检查 UTF-8、乱码特征、HTML 标签、JavaScript 语法、产品预填、提交跳转与线上资源状态。
