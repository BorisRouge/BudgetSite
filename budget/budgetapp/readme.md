Todo list/problems:
1) User should be able to delete selected categories
2) Make it pretty
3) Sidebar? - <nav>html
4) Logout
5) Error if already taken





Solved:
--) The balance of the category doesn change in case of withdraval
--) How to check that balance doesn't go negative? If negative it just does not allow it for the balance, but the ledger changes repeating the previous operation.
--) No Category matches the given query, for user without categores
   (~87)current_category = get_object_or_404(CatModel, user = current_user)
--) Implement selected category
--) Registered user should be automatically logged
