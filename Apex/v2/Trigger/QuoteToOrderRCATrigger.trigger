trigger QuoteToOrderRCATrigger on Quote (after update) {
    if (Trigger.isAfter && Trigger.isUpdate) {
        QuoteToOrderRCATriggerHandler.handleAfterUpdate(Trigger.new, Trigger.oldMap);
    }
}
