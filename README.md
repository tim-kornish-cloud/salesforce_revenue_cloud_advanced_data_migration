Setting up a CPQ migration into Salesforce Revenue Lifecycle management

- reset security token in plaground with:
https://<YourDomain>.lightning.force.com/_ui/system/security/ResetApiTokenEdit



## Phase 1: Global Pricing & Selling Infrastructure

These foundation objects define how products are packaged financially and can be created independently of any physical products or attributes.
1. ProrationPolicy – Defines how subscription pricing splits across fractional periods.
2. ProductSellingModel – Establishes the type of sale (e.g., OneTime, Evergreen, TermDefined).
3. ProductFulfillmentScenario – Outlines how the fulfillment engine treats the product line upon closure.

## Phase 2: Core Attribute Picklists & Schema

Define your product taxonomy and custom characteristics before assigning them to categories.
4. AttributePicklist – The container for custom asset/product properties.
5. AttributePicklistValue – The selective values tied to the picklist (Requires AttributePicklist ID).
6. AttributeDefinition – Links the type of attribute to an AttributePicklist if applicable.
7. AttributeCategory – Groups individual definitions into clean thematic layout containers (e.g., "Hardware Specs").
8. AttributeCategoryAttribute – The junction object mapping AttributeDefinition into AttributeCategory.

## Phase 3: Product Classifications

Set up templates for dynamic attributes prior to establishing actual catalog listings.
9. ProductClassification – Reusable templates holding collections of dynamic attributes.
10. ProductClassificationAttr – Junction mapping attributes directly onto your template classifications.

## Phase 4: Main Product Catalogue & Structure

Now that your financial structures and attribute rules are ready, build the catalog and product entities.
11. ProductCatalog – High-level corporate catalog definition.
12. ProductCategory – Category and subcategory tiers within the active ProductCatalog.
13. Product2 – The actual product record. Note: It looks up to ProductClassification and underlying pricing parameters.

## Phase 5: Product Relationships & Constraints

Apply the structural variations, selling mechanisms, and rules to the finalized Product2 records.
14. ProductSellingModelOption – Connects Product2 to its valid ProductSellingModel options and references the ProrationPolicy.
15. ProductAttributeDefinition – Maps localized attribute definitions directly onto specific Product2 records.



## Quick Summary Table

Phase	      Object Name	                    Primary Dependency / Foreign Key
1	          ProrationPolicy	                None
1	          ProductSellingModel	            None
1	          ProductFulfillmentScenario	    None
2	          AttributePicklist	              None
2	          AttributePicklistValue	        AttributePicklist
2	          AttributeDefinition	            AttributePicklist
2	          AttributeCategory	              None
2	          AttributeCategoryAttribute	    AttributeCategory, AttributeDefinition
3	          ProductClassification	          None
3	          ProductClassificationAttr	      ProductClassification, AttributeDefinition
4	          ProductCatalog	                None
4	          ProductCategory	                ProductCatalog
4	          Product2	                      ProductClassification
5	          ProductSellingModelOption	      Product2, ProductSellingModel, ProrationPolicy
5	          ProductAttributeDefinition	    Product2, AttributeDefinition, AttributeCategory
