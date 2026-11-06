public class QuoteRCAOrderQueueable implements Queueable {
    private Set<Id> quoteIds;

    // Constructor to pass IDs from the trigger context
    public QuoteRCAOrderQueueable(Set<Id> quoteIds) {
        this.quoteIds = quoteIds;
    }

    public void execute(QueueableContext context) {
        for (Id quoteId : this.quoteIds) {
            try {
                // Instantiates the native standard RCA action engine
                Invocable.Action action = Invocable.Action.createStandardAction('createOrdersFromQuote');

                // Set required parameters for standard order generation
                action.setInvocationParameter('quoteId', String.valueOf(quoteId));

                // Options: 'CreateSingleOrder', 'CreateOrderByGroup', or 'CreateOrderByField'
                action.setInvocationParameter('orderCreationMethod', 'CreateSingleOrder');

                // Invoke the execution framework
                List<Invocable.Action.Result> results = action.invoke();

                for (Invocable.Action.Result result : results) {
                    if (!result.isSuccess()) {
                        List<Invocable.Action.Error> errors = result.getErrors();
                        for (Invocable.Action.Error err : errors) {
                            System.debug('RCA Order Generation Failed: ' + err.getMessage());
                        }
                    } else {
                        System.debug('RCA Order successfully created for Quote ID: ' + quoteId);
                    }
                }
            } catch (Exception e) {
                System.debug('RCA Queueable Exception occurred: ' + e.getMessage());
            }
        }
    }
}
