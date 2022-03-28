#define ASSOCIATION_CODE_CH_UUID "2002A7D3-D8A4-4FEA-8174-1736E808C066"
#define IS_ASSOCIATED_CH_UUID "2003A7D3-D8A4-4FEA-8174-1736E808C066"

class AssociationCodeCharacteristic: public BLECharacteristic {
  public:
    AssociationCodeCharacteristic(): BLECharacteristic(BLEUUID(ASSOCIATION_CODE_CH_UUID)) {
    }
};

class IsAssociatedCharacteristic: public BLECharacteristic {
  public:
    IsAssociatedCharacteristic(): BLECharacteristic(BLEUUID(IS_ASSOCIATED_CH_UUID)) {
    }
};
