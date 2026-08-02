# 产品案例模板

案例应使用 `scripts/add_case.py` 从 JSON 写入；手工编辑后必须运行 `scripts/validate_case.py`。

```json
{
  "id": "lowercase-slug",
  "name": "案例名称",
  "source": "来源说明",
  "permission": "是否允许保存和后续引用",
  "original_description": "原始产品描述",
  "target_customer": "目标客户",
  "buying_context": "购买情境",
  "pain": "具体痛点",
  "promise": "结果承诺",
  "format": "产品形态",
  "delivery": "交付机制",
  "duration": "周期",
  "boundaries": "边界",
  "customer_input": "客户配合",
  "pricing": "定价",
  "value_anchor": "价值锚点",
  "trust_evidence": "信任证据",
  "acquisition": "获客与成交方式",
  "transferable_structure": "可迁移结构",
  "non_transferable_conditions": "不可照搬条件",
  "tags": ["客户", "问题", "产品形态"],
  "completeness": "完整 / 部分缺失",
  "confidence": "高 / 中 / 低",
  "recorded_at": "YYYY-MM-DD",
  "updated_at": "YYYY-MM-DD"
}
```

资料缺失时不要编造。用“资料未提供”填写文本字段，将 `completeness` 标为“部分缺失”，并降低 `confidence`。
