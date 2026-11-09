public class QuoteContractCreator {

    public class ContractRequest {
        @InvocableVariable(label='Quote ID' required=true)
        public Id quoteId;

        @InvocableVariable(label='Price Option (CONTRACT_HEADER_ONLY, NET_UNIT_PRICE_ONLY, DISCOUNT_ONLY)')
        public String contractPriceOption;
    }

    @InvocableMethod(label='Create Contract From Quote (RCA)' description='Calls the standard RCA Action to generate a contract from a Quote record.' category='Quote')
    public static void generateContracts(List<ContractRequest> requests) {
        for (ContractRequest req : requests) {
            // Instantiate the standard system Invocable Action for RCA
            Invocable.Action action = Invocable.Action.createStandardAction('createContract');

            // Set the required parameter constraints
            action.setInvocationParameter('sourceId', String.valueOf(req.quoteId));

            if (String.isNotBlank(req.contractPriceOption)) {
                action.setInvocationParameter('contractPriceOption', req.contractPriceOption);
            }

            // Invoke the standard action
            List<Invocable.Action.Result> results = action.invoke();

            // Error handling log validation
            for (Invocable.Action.Result result : results) {
                if (!result.isSuccess()) {
                    for (Invocable.Action.Error error : result.getErrors()) {
                        System.debug('Error creating Contract: ' + error.getMessage());
                    }
                }
            }
        }
    }
}
