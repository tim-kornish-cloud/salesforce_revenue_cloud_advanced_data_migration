public without sharing class QuoteToContractRCATriggerHandler {

    public static void handleAfterUpdate(List<Quote> newQuotes, Map<Id, Quote> oldQuoteMap) {
        Set<Id> quotesToContractIds = new Set<Id>();

        for (Quote newQuote : newQuotes) {
            Quote oldQuote = oldQuoteMap.get(newQuote.Id);

            // verify the checkbox to generate a new contract is set to true
            Boolean fieldWasPopulated = newQuote.Contract_Migrated_Quote__c == true && oldQuote.Contract_Migrated_Quote__c == false;

            // Ensures the quote is in an appropriate status to be converted into an order
            Boolean isValidStatus = (newQuote.Status == 'Approved' || newQuote.Status == 'Accepted');

            if (fieldWasPopulated && isValidStatus) {
                quotesToContractIds.add(newQuote.Id);
            }
        }

        // Enqueue the native asynchronous runner if matching quotes exist
        if (!quotesToContractIds.isEmpty()) {
            System.enqueueJob(new QuoteToContractRCAQueable(quotesToContractIds));
        }
    }
}
