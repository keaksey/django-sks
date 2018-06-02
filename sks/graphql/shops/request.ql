mutation ShopCreate($input: ShopCreateInput!) {
  shopCreate(input: $input) {
    name
  }
}
variable {
    {
      "input": {
        "name": "demo"
      }
    }
}