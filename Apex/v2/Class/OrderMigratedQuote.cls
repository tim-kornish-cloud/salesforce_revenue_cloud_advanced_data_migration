public with sharing class OrderMigratedQuote {
    public static void createOrders(List<Quote> quoteList) {
        Map<Id, Order> quoteToOrderMap = new Map<Id, Order>();
        Set<Id> quoteIds = new Set<Id>();

        // 1. Map Quote Header fields to new Orders
        for (Quote quote : quoteList) {
            quoteIds.add(quote.Id);

            Order order = new Order();
            order.AccountId = quote.AccountId;
            order.OpportunityId = quote.OpportunityId;
            order.QuoteId = quote.Id;
            order.EffectiveDate = Date.today();
            order.Status = 'Draft';
            order.Pricebook2Id = quote.Pricebook2Id; // Must match Quote Pricebook

            quoteToOrderMap.put(quote.Id, order);
        }

        // 2. check if any orders to insert, then insert if map is not empty
        // if no orders to create, break out of function and return nothing
        if (quoteToOrderMap.isEmpty()) return;
        // if there are orders to create, insert orders here
        insert quoteToOrderMap.values();

        // 3. Fetch Quote Line Items ordered by their SortOrder or Sequence
        List<QuoteLineItem> quoteLineItemList = [
            SELECT Id, QuoteId, PricebookEntryId, Quantity, UnitPrice, ListPrice, ServiceDate
            FROM QuoteLineItem
            WHERE QuoteId IN :quoteIds
            ORDER BY SortOrder ASC
        ];

        List<OrderItem> orderItemsToInsert = new List<OrderItem>();

        // 4. Map Quote Lines to Order Items
        for (QuoteLineItem quoteLineItem : quoteLineItemList) {
            Order relatedOrder = quoteToOrderMap.get(quoteLineItem.QuoteId);
            if (relatedOrder != null) {
                OrderItem orderItem = new OrderItem();
                orderItem.OrderId = relatedOrder.Id;
                orderItem.PricebookEntryId = quoteLineItem.PricebookEntryId;
                orderItem.Quantity = quoteLineItem.Quantity;
                orderItem.UnitPrice = quoteLineItem.UnitPrice;
                orderItem.ServiceDate = quoteLineItem.ServiceDate;

                orderItemsToInsert.add(orderItem);
            }
        }
        // 5. Insert all orderItems related to orders that were just inserted above.
        if (!orderItemsToInsert.isEmpty()) {
            insert orderItemsToInsert;
        }
    }
}
