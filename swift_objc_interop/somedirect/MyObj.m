#import "MyObj.h"

@implementation MyObj

- (instancetype)init
{
  if (self = [super init]) {
      _directProp = 123;
      _anotherDirectProp = 456;
  }
  // Uncomment the following line to allow "(lldb) p self.directProp" to work.
  // NSInteger a = self.directProp;
  return self; // breakpoint here to stop in Objective-C
}

@end
