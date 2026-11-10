Setting up a CPQ migration into Salesforce Revenue Lifecycle management

- reset security token in plaground with:
https://<YourDomain>.lightning.force.com/_ui/system/security/ResetApiTokenEdit

The correct structural order of creation is:
1. AttributeCategory
  - (Top-level grouping)
  - No required parent
2. AttributePicklist
  - (Independent container for dropdown values)
  - No required parent
3. AttributePicklistValue
  - (Children of the Picklist; requires AttributePicklist)
  - requires: AttributePicklist
4. AttributeDefinition
  - (The global definition of the attribute; requires AttributeCategory and optionally AttributePicklist)
  - requires: AttributeCategory, AttributePicklist (optional)
5. ProductClassification
  - (The catalog/class grouping category)
  - No required parent
6. ProductClassificationAttr
  - (Binds the definition to the classification category; requires ProductClassification and AttributeDefinition)
  - requires: ProductClassification, AttributeDefinition
7. ProductAttributeDefinition
  - (The actual instance on a specific product; requires AttributeDefinition)
  - requires: AttributeDefinition, Product2 (or your specific catalog item)
