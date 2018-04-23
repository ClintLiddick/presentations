#include <string>

#include "image.pb.h"

void serialize_image(const std::string &path, std::string *data_out) {
  // Load data...
  const auto img = load_image(path);
  ImageMsg msg{};
  msg.set_original_filename(img.name);
  msg.set_width(img.width);
  msg.set_height(img.height);
  msg.mutable_image_data() = img.data;

  msg.SerializeToString(data_out);
}
