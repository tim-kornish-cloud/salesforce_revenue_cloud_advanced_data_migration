public class QuoteToContractRCAQueable implements Queueable {
    private Set<Id> quoteIds;

    // Constructor to pass IDs from the trigger context
    public QuoteToContractRCAQueable(Set<Id> quoteIds) {
        this.quoteIds = quoteIds;
    }

    public void execute(QueueableContext context) {
        for (Id quoteId : this.quoteIds) {
            try {
                // Instantiates the native standard RCA action engine
                Invocable.Action action = Invocable.Action.createStandardAction('createContractFromQuote');

                // Set the required parameter constraints for contract generation
                action.setInvocationParameter('sourceId', String.valueOf(quoteId));

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
            } catch (Exception e) {
                System.debug('RCA Queueable Exception occurred: ' + e.getMessage());
            }
        }
    }
}
