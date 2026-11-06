trigger QuoteTrigger on Quote (after update) {
    List<Quote> quotesToOrder = new List<Quote>();

    for (Quote quote : Trigger.new) {
        Quote oldQuote = Trigger.oldMap.get(quote.Id);

        // Trigger condition: Checkbox flipped to true
        if (quote.Order_Migrated_Quote__c == true && oldQuote.Order_Migrated_Quote__c == false) {
            quotesToOrder.add(quote);
        }
    }

    if (!quotesToOrder.isEmpty()) {
        OrderMigratedQuote.createOrders(quotesToOrder);
    }
}
