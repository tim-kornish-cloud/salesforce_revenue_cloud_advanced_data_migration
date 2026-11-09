trigger QuoteContractTrigger on Quote (after update) {
    List<QuoteContractCreator.ContractRequest> requestsToProcess = new List<QuoteContractCreator.ContractRequest>();

    for (Quote newQuote : Trigger.new) {
        Quote oldQuote = Trigger.oldMap.get(newQuote.Id);

        // verify the checkbox to generate a new order is set to true
        Boolean fieldWasPopulated = newQuote.Contract_Migrated_Quote__c == true && oldQuote.Contract_Migrated_Quote__c == false;

        // Ensures the quote is in an appropriate status to be converted into an order
        Boolean isValidStatus = (newQuote.Status == 'Approved' || newQuote.Status == 'Accepted');


        // Trigger condition: Run when Status transitions to 'Accepted'
        if (fieldWasPopulated && isValidStatus) {
            QuoteContractCreator.ContractRequest req = new QuoteContractCreator.ContractRequest();
            req.quoteId = newQuote.Id;
            req.contractPriceOption = ''; //'NET_UNIT_PRICE_ONLY'; // Options: CONTRACT_HEADER_ONLY, NET_UNIT_PRICE_ONLY, DISCOUNT_ONLY
            requestsToProcess.add(req);
        }
    }

    if (!requestsToProcess.isEmpty()) {
        // Enqueue or run action handler
        QuoteContractCreator.generateContracts(requestsToProcess);
    }
}
