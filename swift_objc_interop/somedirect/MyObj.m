#import "MyObj.h"

@implementation MyObj

- (instancetype)init
{
  if (self = [super init]) {
      _directProp = 123;
      _anotherDirectProp = 456;
  }
  return self; // breakpoint here to stop in Objective-C
}

@end
