public with sharing class QuoteToContractRCATriggerHandler {

    public static void handleAfterUpdate(List<Quote> newQuotes, Map<Id, Quote> oldQuoteMap) {
        Set<Id> quotesToOrderIds = new Set<Id>();

        for (Quote newQuote : newQuotes) {
            Quote oldQuote = oldQuoteMap.get(newQuote.Id);

            // Replace 'Your_Custom_Field__c' with your actual custom field API name
            Boolean fieldWasPopulated = newQuote.Order_Migrated_Quote__c == true && oldQuote.Order_Migrated_Quote__c == false;

            // Ensures the quote is in an appropriate status to be converted into an order
            Boolean isValidStatus = (newQuote.Status == 'Approved' || newQuote.Status == 'Accepted');

            if (fieldWasPopulated && isValidStatus) {
                quotesToOrderIds.add(newQuote.Id);
            }
        }

        // Enqueue the native asynchronous runner if matching quotes exist
        if (!quotesToOrderIds.isEmpty()) {
            System.enqueueJob(new QuoteToContractRCAQueable(quotesToOrderIds));
        }
    }
}
