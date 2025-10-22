"""
Hair Disease Classification Training Script
Using ImageNet Pre-trained ResNet50 with Transfer Learning

This script will train a ResNet50 model on your hair disease dataset
and save the trained model for use in your SwasthVedha application.
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import torchvision
from torchvision import datasets, transforms, models
import numpy as np
import matplotlib.pyplot as plt
import json
import os
from pathlib import Path
import time
import copy
from datetime import datetime
import logging

# Setup logging with UTF-8 encoding for Windows
try:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('hair_training.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
except Exception:
    # Fallback without Unicode characters for Windows compatibility
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('hair_training.log'),
            logging.StreamHandler()
        ]
    )
logger = logging.getLogger(__name__)

class HairDiseaseTrainer:
    """Complete trainer for hair disease classification using ResNet50"""
    
    def __init__(self, dataset_path, output_dir="models"):
        """
        Initialize the trainer
        
        Args:
            dataset_path: Path to the hair disease dataset
            output_dir: Directory to save trained models
        """
        self.dataset_path = Path(dataset_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Training configuration
        self.batch_size = 16
        self.num_epochs = 25
        self.learning_rate = 0.001
        self.num_workers = 4
        
        # Device configuration
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Using device: {self.device}")
        
        # Model and training objects
        self.model = None
        self.criterion = None
        self.optimizer = None
        self.scheduler = None
        self.class_names = []
        self.class_to_idx = {}
        
        # Training history
        self.train_losses = []
        self.val_losses = []
        self.train_accuracies = []
        self.val_accuracies = []
        
    def setup_data_transforms(self):
        """Setup data transformations for training and validation"""
        
        # Data transformations
        self.data_transforms = {
            'train': transforms.Compose([
                transforms.Resize((256, 256)),
                transforms.RandomResizedCrop(224, scale=(0.8, 1.0)),
                transforms.RandomHorizontalFlip(p=0.5),
                transforms.RandomRotation(degrees=15),
                transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ]),
            'val': transforms.Compose([
                transforms.Resize((256, 256)),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ]),
            'test': transforms.Compose([
                transforms.Resize((256, 256)),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ])
        }
        
        logger.info("Data transformations configured")
    
    def load_datasets(self):
        """Load the hair disease datasets"""
        
        logger.info("Loading datasets...")
        
        # Load datasets
        self.image_datasets = {}
        self.dataloaders = {}
        self.dataset_sizes = {}
        
        for phase in ['train', 'val', 'test']:
            dataset_path = self.dataset_path / phase
            
            if not dataset_path.exists():
                logger.error(f"Dataset path not found: {dataset_path}")
                raise FileNotFoundError(f"Dataset path not found: {dataset_path}")
            
            self.image_datasets[phase] = datasets.ImageFolder(
                dataset_path,
                self.data_transforms[phase]
            )
            
            # Shuffle only for training
            shuffle = (phase == 'train')
            
            self.dataloaders[phase] = DataLoader(
                self.image_datasets[phase],
                batch_size=self.batch_size,
                shuffle=shuffle,
                num_workers=self.num_workers,
                pin_memory=True if self.device.type == 'cuda' else False
            )
            
            self.dataset_sizes[phase] = len(self.image_datasets[phase])
            
            logger.info(f"{phase.capitalize()} dataset: {self.dataset_sizes[phase]} images")
        
        # Get class names and create mappings
        self.class_names = self.image_datasets['train'].classes
        self.class_to_idx = self.image_datasets['train'].class_to_idx
        self.num_classes = len(self.class_names)
        
        logger.info(f"Found {self.num_classes} classes: {self.class_names}")
        
        return self.dataloaders, self.dataset_sizes
    
    def create_model(self):
        """Create ResNet50 model with ImageNet pre-trained weights"""
        
        logger.info("Creating ResNet50 model with ImageNet pre-trained weights...")
        
        # Load pre-trained ResNet50
        self.model = models.resnet50(weights='IMAGENET1K_V1')
        
        # Freeze early layers for transfer learning
        for param in self.model.parameters():
            param.requires_grad = False
        
        # Unfreeze the last residual block and final layers
        for param in self.model.layer4.parameters():
            param.requires_grad = True
        
        # Replace the final fully connected layer
        num_ftrs = self.model.fc.in_features
        self.model.fc = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(num_ftrs, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, self.num_classes)
        )
        
        # Move model to device
        self.model = self.model.to(self.device)
        
        # Print model info
        total_params = sum(p.numel() for p in self.model.parameters())
        trainable_params = sum(p.numel() for p in self.model.parameters() if p.requires_grad)
        
        logger.info(f"Model created successfully")
        logger.info(f"Total parameters: {total_params:,}")
        logger.info(f"Trainable parameters: {trainable_params:,}")
        
        return self.model
    
    def setup_training(self):
        """Setup loss function, optimizer, and scheduler"""
        
        # Loss function
        self.criterion = nn.CrossEntropyLoss()
        
        # Optimizer - only optimize parameters that require gradients
        self.optimizer = optim.AdamW(
            filter(lambda p: p.requires_grad, self.model.parameters()),
            lr=self.learning_rate,
            weight_decay=0.01
        )
        
        # Learning rate scheduler
        self.scheduler = optim.lr_scheduler.StepLR(
            self.optimizer,
            step_size=7,
            gamma=0.1
        )
        
        logger.info("Training setup completed")
    
    def train_epoch(self, phase):
        """Train or validate for one epoch"""
        
        if phase == 'train':
            self.model.train()
        else:
            self.model.eval()
        
        running_loss = 0.0
        running_corrects = 0
        
        # Iterate over data
        for inputs, labels in self.dataloaders[phase]:
            inputs = inputs.to(self.device)
            labels = labels.to(self.device)
            
            # Zero the parameter gradients
            self.optimizer.zero_grad()
            
            # Forward pass
            with torch.set_grad_enabled(phase == 'train'):
                outputs = self.model(inputs)
                _, preds = torch.max(outputs, 1)
                loss = self.criterion(outputs, labels)
                
                # Backward pass + optimize only if in training phase
                if phase == 'train':
                    loss.backward()
                    self.optimizer.step()
            
            # Statistics
            running_loss += loss.item() * inputs.size(0)
            running_corrects += torch.sum(preds == labels.data)
        
        if phase == 'train':
            self.scheduler.step()
        
        epoch_loss = running_loss / self.dataset_sizes[phase]
        epoch_acc = running_corrects.double() / self.dataset_sizes[phase]
        
        return epoch_loss, epoch_acc
    
    def train_model(self):
        """Complete training loop"""
        
        logger.info(f"Starting training for {self.num_epochs} epochs...")
        logger.info(f"Training on {self.dataset_sizes['train']} images")
        logger.info(f"Validating on {self.dataset_sizes['val']} images")
        
        since = time.time()
        best_model_wts = copy.deepcopy(self.model.state_dict())
        best_acc = 0.0
        best_epoch = 0
        
        for epoch in range(self.num_epochs):
            epoch_start = time.time()
            
            logger.info(f'Epoch {epoch+1}/{self.num_epochs}')
            logger.info('-' * 40)
            
            # Each epoch has a training and validation phase
            for phase in ['train', 'val']:
                epoch_loss, epoch_acc = self.train_epoch(phase)
                
                # Store metrics
                if phase == 'train':
                    self.train_losses.append(epoch_loss)
                    self.train_accuracies.append(epoch_acc)
                else:
                    self.val_losses.append(epoch_loss)
                    self.val_accuracies.append(epoch_acc)
                
                logger.info(f'{phase.capitalize()} Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}')
                
                # Deep copy the model if it's the best so far
                if phase == 'val' and epoch_acc > best_acc:
                    best_acc = epoch_acc
                    best_epoch = epoch
                    best_model_wts = copy.deepcopy(self.model.state_dict())
            
            epoch_time = time.time() - epoch_start
            logger.info(f'Epoch {epoch+1} completed in {epoch_time:.0f}s')
            logger.info(f'Best val Acc so far: {best_acc:.4f} at epoch {best_epoch+1}')
            print()
        
        time_elapsed = time.time() - since
        logger.info(f'Training completed in {time_elapsed // 60:.0f}m {time_elapsed % 60:.0f}s')
        logger.info(f'Best val Accuracy: {best_acc:.4f} at epoch {best_epoch+1}')
        
        # Load best model weights
        self.model.load_state_dict(best_model_wts)
        
        return self.model
    
    def evaluate_model(self):
        """Evaluate the model on test set"""
        
        logger.info("Evaluating model on test set...")
        
        self.model.eval()
        test_corrects = 0
        test_total = 0
        class_correct = list(0. for i in range(self.num_classes))
        class_total = list(0. for i in range(self.num_classes))
        
        with torch.no_grad():
            for inputs, labels in self.dataloaders['test']:
                inputs = inputs.to(self.device)
                labels = labels.to(self.device)
                
                outputs = self.model(inputs)
                _, predicted = torch.max(outputs, 1)
                
                test_total += labels.size(0)
                test_corrects += (predicted == labels).sum().item()
                
                # Per-class accuracy
                c = (predicted == labels).squeeze()
                for i in range(labels.size(0)):
                    label = labels[i]
                    class_correct[label] += c[i].item()
                    class_total[label] += 1
        
        test_accuracy = 100 * test_corrects / test_total
        logger.info(f'Test Accuracy: {test_accuracy:.2f}%')
        
        # Per-class accuracy
        logger.info("Per-class accuracy:")
        for i in range(self.num_classes):
            if class_total[i] > 0:
                acc = 100 * class_correct[i] / class_total[i]
                logger.info(f'  {self.class_names[i]}: {acc:.2f}%')
        
        return test_accuracy
    
    def save_model(self, test_accuracy):
        """Save the trained model and related files"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save model state dict
        model_path = self.output_dir / "hair_resnet50.pth"
        
        # Prepare model artifacts
        model_artifacts = {
            'model_state_dict': self.model.state_dict(),
            'class_to_idx': self.class_to_idx,
            'class_names': self.class_names,
            'model_info': {
                'architecture': 'ResNet50',
                'num_classes': self.num_classes,
                'input_size': 224,
                'test_accuracy': test_accuracy,
                'training_date': timestamp,
                'batch_size': self.batch_size,
                'num_epochs': self.num_epochs,
                'learning_rate': self.learning_rate,
                'pretrained_source': 'ImageNet'
            }
        }
        
        torch.save(model_artifacts, model_path)
        logger.info(f"Model saved to: {model_path}")
        
        # Save class mapping for the hair router
        class_mapping_path = self.output_dir / "hair_class_mapping.json"
        with open(class_mapping_path, 'w') as f:
            json.dump(self.class_names, f, indent=2)
        logger.info(f"Class mapping saved to: {class_mapping_path}")
        
        # Save detailed model info
        model_info_path = self.output_dir / "hair_model_info.json"
        with open(model_info_path, 'w') as f:
            json.dump(model_artifacts['model_info'], f, indent=2)
        logger.info(f"Model info saved to: {model_info_path}")
        
        # Save training history
        history = {
            'train_losses': [float(x) for x in self.train_losses],
            'val_losses': [float(x) for x in self.val_losses],
            'train_accuracies': [float(x) for x in self.train_accuracies],
            'val_accuracies': [float(x) for x in self.val_accuracies],
        }
        
        history_path = self.output_dir / "training_history.json"
        with open(history_path, 'w') as f:
            json.dump(history, f, indent=2)
        logger.info(f"Training history saved to: {history_path}")
        
        return model_path
    
    def plot_training_history(self):
        """Plot training history"""
        
        try:
            plt.figure(figsize=(12, 4))
            
            # Plot training & validation accuracy
            plt.subplot(1, 2, 1)
            epochs = range(1, len(self.train_accuracies) + 1)
            plt.plot(epochs, [float(x) for x in self.train_accuracies], 'b-', label='Training Accuracy')
            plt.plot(epochs, [float(x) for x in self.val_accuracies], 'r-', label='Validation Accuracy')
            plt.title('Model Accuracy')
            plt.xlabel('Epoch')
            plt.ylabel('Accuracy')
            plt.legend()
            plt.grid(True)
            
            # Plot training & validation loss
            plt.subplot(1, 2, 2)
            plt.plot(epochs, self.train_losses, 'b-', label='Training Loss')
            plt.plot(epochs, self.val_losses, 'r-', label='Validation Loss')
            plt.title('Model Loss')
            plt.xlabel('Epoch')
            plt.ylabel('Loss')
            plt.legend()
            plt.grid(True)
            
            plt.tight_layout()
            
            # Save plot
            plot_path = self.output_dir / "training_history.png"
            plt.savefig(plot_path, dpi=300, bbox_inches='tight')
            logger.info(f"Training history plot saved to: {plot_path}")
            
            plt.show()
            
        except Exception as e:
            logger.warning(f"Could not create training plots: {e}")
    
    def run_complete_training(self):
        """Run the complete training pipeline"""
        
        try:
            # Setup
            logger.info("Starting Hair Disease Classification Training")
            logger.info(f"Dataset path: {self.dataset_path}")
            logger.info(f"Output directory: {self.output_dir}")
            
            # Step 1: Setup data transformations
            self.setup_data_transforms()
            
            # Step 2: Load datasets
            self.load_datasets()
            
            # Step 3: Create model
            self.create_model()
            
            # Step 4: Setup training
            self.setup_training()
            
            # Step 5: Train model
            self.train_model()
            
            # Step 6: Evaluate model
            test_accuracy = self.evaluate_model()
            
            # Step 7: Save model
            model_path = self.save_model(test_accuracy)
            
            # Step 8: Plot training history
            self.plot_training_history()
            
            # Final summary
            logger.info("Training completed successfully!")
            logger.info(f"Final test accuracy: {test_accuracy:.2f}%")
            logger.info(f"Model saved to: {model_path}")
            logger.info(f"All files saved to: {self.output_dir}")
            
            return {
                'model_path': model_path,
                'test_accuracy': test_accuracy,
                'class_names': self.class_names,
                'num_classes': self.num_classes
            }
            
        except Exception as e:
            logger.error(f"Training failed with error: {str(e)}")
            raise

def main():
    """Main function to run training"""
    
    print("Hair Disease Classification - ResNet50 Training")
    print("=" * 60)
    
    # Get dataset path
    dataset_path = input("Enter path to hair disease dataset (or press Enter for default): ").strip()
    if not dataset_path:
        dataset_path = r"C:\Users\Chethan\Downloads\archive (16)\Hair Diseases - Final"
    
    print(f"Using dataset: {dataset_path}")
    
    # Verify dataset exists
    if not Path(dataset_path).exists():
        print(f"Dataset path not found: {dataset_path}")
        print("Please check the path and try again.")
        return
    
    # Create trainer and run training
    try:
        trainer = HairDiseaseTrainer(dataset_path)
        results = trainer.run_complete_training()
        
        print("\n" + "=" * 60)
        print("TRAINING COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print(f"Test Accuracy: {results['test_accuracy']:.2f}%")
        print(f"Classes: {results['num_classes']}")
        print(f"Model saved to: {results['model_path']}")
        print("\nNext steps:")
        print("1. The trained model is ready to use in your SwasthVedha app")
        print("2. Model files are saved in the 'models' directory")
        print("3. Your hair analysis router will automatically detect the new model")
        
    except Exception as e:
        print(f"\nTraining failed: {str(e)}")
        print("Check the logs for detailed error information.")

if __name__ == "__main__":
    main()